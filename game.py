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
try:
    import simplejson as json
except ImportError:
    import json

import Tkinter as tk
from twisted.internet import  protocol, reactor, tksupport
from twisted.protocols.basic import LineReceiver
from config import config
from messages import move, reset

__all__ = [
    'factory', 'Game', 'game', 'GameProtocol', 'keypress', 'root', 'stats',
    'types'
]

# Graphically display a character or chip's type.
types = {
    'air': 'A',
    'none': 'N',
    'plus': 'P'
}

class Game(object):
    """Contains the game's data."""
    def __init__(self):
        """Create the initial game data."""
        module = __import__(
            'characters.%s' % (config['character']),
            globals(),
            locals(),
            ('Character',),
            -1
        )
        self.player = module.Character(self)
        self.opponent = module.Character(self, col=4)
        self.field = []
        for row in range(0, 3):
            cols = []
            for col in range(0, 6):
                character = None
                if row == 1:
                    if col == 1:
                        character = self.player
                    if col == 4:
                        character = self.opponent
                panel = {
                    'character': character,
                    'stolen': False,
                    'status': 'normal',
                    'time': 0
                }
                cols.append(panel)
            self.field.append(cols)
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

    def draw(self):
        """Draw the screen"""
        # Start by clearing the screen.
        os.system('cls')
        # If the player is prompted to select a chip
        if self.select:
            # Display the chip selection.
            menu = 'Custom: '
            for key, chip in enumerate(self.picked):
                menu += '|'
                cursor = '  '
                if key == self.selection:
                    cursor = '+ '
                menu += cursor
                power = ''
                if hasattr(self.chips[chip], 'power'):
                    power = ' %s' % (self.chips[chip].power)
                equipable = self.equipable(key)
                if equipable:
                    equipable = ' '
                else:
                    equipable = 'X'
                if not key in self.selected:
                    menu += '%s%s %s %s %s' % (
                        self.chips[chip].name,
                        power,
                        types[self.chips[chip].type],
                        self.chips[chip].code,
                        equipable
                    )
                else:
                    menu += '%s%s %s %s %s' % (
                        ' ' * len(self.chips[chip].name),
                        ' ' * len(str(power)),
                        ' ' * len(types[self.chips[chip].type]),
                        ' ' * len(self.chips[chip].code),
                        ' ' * len(equipable)
                    )
            if self.picked:
                menu += '|'
            print menu
        # Display the custom bar.
        custom = ''
        # If the bar is full, display a message.
        if self.custombar >= 10:
            custom = ' Custom'
        print '%s%s' % (('*' * self.custombar), custom)
        grid = ''
        for row in self.field:
            grid += '\n ----- ----- ----- ----- ----- -----'
            grid += '\n|'
            for key, col in enumerate(row):
                label = ' '
                red = ' '
                status = {
                    'broken': 'B',
                    'cracked': 'C',
                    'grass': 'G',
                    'holy': 'H',
                    'ice': 'I',
                    'lava': 'L',
                    'normal': ' ',
                    'metal': 'M',
                    'poison': 'P',
                    'sand': 'S',
                    'water': 'W'
                }
                # Place all living characters.
                if col['character'] and col['character'].health:
                    label = 'x'
                    # If the player is this character, change the symbol.
                    if col['character'] == self.player:
                        label = 'o'
                # Label a red panels.
                if (
                    (key > 2 and not col['stolen']) or
                    (key < 3 and col['stolen'])
                ):
                    red = 'R'
                grid += ' %s%s%s |' % (status[col['status']], label, red)
            grid += '\n ----- ----- ----- ----- ----- -----'
        print grid
        stats(self.player)
        stats(self.opponent)
        # If the game is over, display the winner and loser and prompt
        # restarting.
        if not self.player.health or not self.opponent.health:
            winner = self.player
            loser = self.opponent
            if not self.player.health:
                winner = self.opponent
                loser = self.player
            print '\n%s defeated! %s wins! Press "r" to restart.' % (
                loser.name,
                winner.name
            )
        print '\nControls:'
        print 'Directional Keys - Move Player / Chip Selection'
        print 'A: Use / Select Chip'
        print 'S: Use Buster / Remove Chip'
        print 'D: Prompt Chip Selection'
        print 'C: Charge Shot'
        print 'T: Advance time (Test)'
        print 'F: Deal 25 damage to player (Test)'
        print 'G: Deal 100 damage to player (Test)'
        print 'Enter: End Chip Selection'
        print 'Escape - End Game'

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
        for row in self.field:
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

    def send(self, line):
        """Messages are always to be sent as a JSON string."""
        self.sendLine(json.dumps(line))

    def lineReceived(self, line):
        line = json.loads(line)
        if 'blue' in line and config['blue'] != line['blue']:
            line['col'] = range(5, -1, -1)[line['col']]
            if line['function'] == 'move':
                line['rows'] = -line['rows']
        character = game.field[line['row']][line['col']]['character']
        for key, value in line['kwargs'].items():
            del line['kwargs'][key]
            line['kwargs'][str(key)] = value
        getattr(character, line['function'])(**line['kwargs'])
        game.draw()
        if line['reset']:
            reset()

def keypress(event):
    """Handle a key press."""
    key = event.keysym
    if key == 'Escape':
        # Prepare to exit.
        root.destroy()
    # If the game is not over
    if game.player.health and game.opponent.health:
        # If the player is prompted to select a chip
        if game.select:
            if key == 'Return':
                # Finish the selection.
                game.select = False
                # Add the chips to the player.
                for value in game.selected:
                    game.player.chips.append(game.chips[game.picked[value]])
                # Make the first selected the first used.
                game.player.chips.reverse()
                # Remove the chips from the library.
                game.selected.sort()
                offset = 0
                for value in game.selected:
                    del game.chips[game.picked[value] - offset]
                    offset += 1
            if key == 'Right':
                game.cursor(1)
            if key == 'Left':
                game.cursor(-1)
            if key == 'a' and game.equipable(game.selection):
                # Prepare to add the chip.
                game.selected.append(game.selection)
            if key == 's' and game.selected:
                # Undo the selection.
                game.selected.pop()
        else:
            if key == 't':
                game.time()
            if key == 'Up':
                move(game.player, rows=1)
            if key == 'Down':
                move(game.player, rows=-1)
            if key == 'Right':
                move(game.player, cols=1)
            if key == 'Left':
                move(game.player, cols=-1)
            if key == 'a' and game.player.chips:
                game.player.usechip()
            if key == 's':
                game.player.buster()
            if key == 'd':
                # Start the selection if the custom bar is full.
                if game.custombar == 10:
                    game.custom()
            if key == 'c':
                game.player.charge()
            if key == 'f':
                game.player.hit(25)
            if key == 'g':
                game.player.hit(100)
    elif key == 'r':
        game.__init__()
    game.draw()

def stats(character):
    """Draw a character's statistics."""
    print '\n%s' % (character.name)
    print '-HP: %s' % (str(character.health))
    print '-Status: %s' % (', '.join(character.status))
    print '-Type: %s' % (character.type)
    chips = []
    # Display the usable chips.
    for value in character.chips:
        power = ''
        if hasattr(value, 'power'):
            power = ' %s' % (value.power)
        chips.append('%s%s %s' % (value.name, power, types[value.type]))
    print '-Chips: %s' % (', '.join(chips))
    print '-Active Chip:'
    # Display the active chips.
    for key, type in character.activechips.items():
        if type:
            names = []
            if isinstance(type, dict):
                type = list(dict([(v, k) for (k, v) in type.iteritems()]))
            for chip in type:
                names.append(chip.name)
            print '--%s: %s' % (key, ', '.join(names))

game = Game()
factory = protocol.ClientFactory()
factory.protocol = GameProtocol
game.draw()
root = tk.Tk()
tksupport.install(root)
root.bind_all('<Key>', keypress)
root.withdraw()
reactor.connectTCP('localhost', 9634, factory)
reactor.run()