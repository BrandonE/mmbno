# -*- coding: utf-8 -*-
# This file is part of MMBN Online
# MMBN Online is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# MMBN Online is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with MMBN Online.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2008-2010 Chris Santiago and Brandon Evans.
# http://mmbnonline.net/

"""Contains the game's data."""

import os
from random import randint, shuffle
from pprint import pprint
try:
    import simplejson as json
except ImportError:
    import json

from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

from messages import move
from field import flipfield, makefield
from config import config

__all__ = ['factory', 'Game', 'game', 'GameProtocol']

class Game(object):
    """Contains the game's data."""
    def __init__(self):
        """Create the initial game data."""
        field = makefield()
        opponentfield = flipfield(field)
        from characters.mega import Character
        self.player = Character(self, field)
        from characters.bass import Character
        self.opponent = Character(self, opponentfield)
        field[0][0]['status'] = 'broken'
        field[0][1]['status'] = 'grass'
        field[0][2]['status'] = 'poison'
        field[0][5]['status'] = 'broken'
        field[1][0]['status'] = 'cracked'
        field[1][1]['status'] = 'ice'
        field[1][2]['status'] = 'holy'
        field[2][0]['status'] = 'lava'
        field[1][4]['status'] = 'grass'
        self.chips = json.loads(
            open(
                os.path.join(
                    'chips',
                    'folders',
                    '%s.json' % (config['chipfolder'])
                )
            ).read()
        )
        if len(self.chips) > 30:
            raise Exception('Your folder cannot have more than 30 chips.')
        if len(self.chips) < 30:
            raise Exception('Your folder must have 30 chips.')
        # Convert the list of chip names and codes to a list of chip instances.
        for key, value in enumerate(self.chips):
            chip = 'chips.%s' % (value['chip'])
            module = __import__(chip, globals(), locals(), ('Chip',), -1)
            self.chips[key] = module.Chip(self.player, value)
            if not value['code'] in self.chips[key].codes:
                raise Exception('Improper chip code')
            self.chips[key].code = value['code']
        self.custom()

    def cursor(self, cols):
        """Move the cursor for chip selection."""
        newcol = self.selection + cols
        if newcol >= 0 and newcol < len(self.picked):
            self.selection = newcol

    def custom(self):
        """Redefine all the necessary values when prompting the custom bar."""
        self.custombar = 0
        self.player.chips = []
        self.pickchips()
        self.select = True
        self.selection = 0
        self.selected = []

    def equipable(self, chip):
        """Check if a chip can be equipped."""
        # If the chip has already been selected, you have already selected
        # five, or the chip is out of range.
        if (
            chip in self.selected or
            len(self.selected) > 4 or
            chip > len(self.chips) - 1
        ):
            return
        # Add the chip in question to see if the new set fits the conditions.
        self.selected.append(chip)
        chip = game.chips[game.picked[chip]]
        codes = set([])
        names = set([])
        success = True
        for value in self.selected:
            thischip = self.chips[self.picked[value]]
            if thischip.code != '*':
                codes.add(thischip.code)
            names.add(thischip.name)
            # If you have two different names and two different codes, fail.
            if len(names) > 1 and len(codes) > 1:
                success = False
                break
        # Remove the chip.
        self.selected.pop()
        return success

    def pickchips(self):
        """Pick a certain amount of random chips for selection."""
        picked = set([])
        # While there are chips to pick and the list is under 10, pick.
        while len(self.chips) != len(picked) and len(picked) < 10:
            picked.add(randint(0, len(self.chips) - 1))
        self.picked = list(picked)
        shuffle(self.picked)

    def time(self):
        """Handle a unit of time."""
        # Fill the custom bar if not full.
        if self.custombar != 10:
            self.custombar += 1
        for row in self.player.field:
            for panel in row:
                # If the panel is broken
                if panel['status'] == 'broken':
                    # Prepare to restore.
                    panel['time'] += 1
                    # Restore if ready.
                    if panel['time'] == 10:
                        panel['status'] = 'normal'
                        panel['time'] = 0
        # Have the player and opponent run handle a unit of time.
        self.player.time()
        self.opponent.time()

class GameProtocol(LineReceiver):
    """Client for Twisted Server."""
    def connectionMade(self):
        reactor.protocol = self
        self.positionPlayers()

    def positionPlayers(self):
        """Position the two players at the start of the match."""
        move(game.player, force=True)
        move(game.opponent, force=True)

    def send(self, line):
        """Messages are always to be sent as a JSON string."""
        self.sendLine('%s%s' % (json.dumps(line), self.delimiter))

    def lineReceived(self, line):
        line = json.loads(line)

        if 'blue' in line and config['blue'] != line['blue']:
            line['col'] = range(5, -1, -1)[line['col']]
            if line['function'] == 'move':
                line['rows'] = -line['rows']
        character = game.field[line['row']][line['col']]['character']
        getattr(character, line['function'])(**line['kwargs'])

game = Game()
factory = protocol.ClientFactory()
factory.protocol = GameProtocol