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
try:
    import simplejson as json
except ImportError:
    import json

import Tkinter as tk
from twisted.internet import  protocol, reactor, tksupport
from twisted.protocols.basic import LineReceiver
from config import config
from game import Game
from messages import move

__all__ = [
    'draw', 'factory', 'GameProtocol', 'keypress', 'root', 'properties',
    'types'
]

# Graphically display a character or chip's type.
types = {
    'air': 'A',
    'none': 'N',
    'plus': 'P'
}

class GameProtocol(LineReceiver):
    """Client for Twisted Server."""
    def connectionMade(self):
        reactor.protocol = self
        draw(reactor.game)

    def send(self, line):
        """Messages are always to be sent as a JSON string."""
        self.sendLine(json.dumps(line))

    def lineReceived(self, line):
        line = json.loads(line)
        for key, value in line['kwargs'].items():
            del line['kwargs'][key]
            line['kwargs'][str(key)] = value
        if (
            line['function'] == 'move' and
            config['blue'] != line['kwargs']['blue']
        ):
            line['kwargs']['cols'] = -line['kwargs']['cols']
        if line['object'] == 'character':
            if line['id'] == reactor.game.player.id:
                callable = reactor.game.player
            if line['id'] == reactor.game.opponent.id:
                callable = reactor.game.opponent
        if line['object'] == 'game':
            callable = reactor.game
        getattr(callable, line['function'])(**line['kwargs'])
        draw(reactor.game)

def draw(game):
    """Draw the screen"""
    # Start by clearing the screen.
    os.system('cls')
    # If the player is prompted to select a chip
    if game.select:
        # Display the chip selection.
        menu = 'Custom: '
        for key, chip in enumerate(game.picked):
            menu += '|'
            cursor = '  '
            if key == game.selection:
                cursor = '+ '
            menu += cursor
            power = ''
            if hasattr(game.chips[chip], 'power'):
                power = ' %s' % (game.chips[chip].power)
            equipable = game.equipable(key)
            if equipable:
                equipable = ' '
            else:
                equipable = 'X'
            if not key in game.selected:
                menu += '%s%s %s %s %s' % (
                    game.chips[chip].name,
                    power,
                    types[game.chips[chip].type],
                    game.chips[chip].code,
                    equipable
                )
            else:
                menu += '%s%s %s %s %s' % (
                    ' ' * len(game.chips[chip].name),
                    ' ' * len(str(power)),
                    ' ' * len(types[game.chips[chip].type]),
                    ' ' * len(game.chips[chip].code),
                    ' ' * len(equipable)
                )
        if game.picked:
            menu += '|'
        print menu
    print 'Players: %s' % (game.players)
    # Display the custom bar.
    custom = ''
    # If the bar is full, display a message.
    if game.custombar >= 10:
        custom = ' Custom'
    print '%s%s' % (('*' * game.custombar), custom)
    grid = ''
    for row in game.field:
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
                if col['character'] == game.player:
                    label = 'o'
            # Label a red panels.
            if (key > 2) ^ col['stolen']:
                red = 'R'
            grid += ' %s%s%s |' % (status[col['status']], label, red)
        grid += '\n ----- ----- ----- ----- ----- -----'
    print grid
    properties(game.player)
    properties(game.opponent)
    # If the game is over, display the winner and loser and prompt
    # restarting.
    if not game.player.health or not game.opponent.health:
        winner = game.player
        loser = game.opponent
        if not game.player.health:
            winner = game.opponent
            loser = game.player
        print '\n%s defeated! %s wins! Press "r" to restart.' % (
            loser.name,
            winner.name
        )
    print '\nControls:'
    print 'Directional Keys - Move Player / Chip Selection'
    print 'A - Use / Select Chip'
    print 'S - Use Buster / Remove Chip'
    print 'D - Prompt Chip Selection'
    print 'C - Charge Shot'
    print 'F - Go forward time'
    print 'Enter - End Chip Selection'
    print 'Escape - End Game'

def keypress(event):
    """Handle a key press."""
    key = event.keysym
    if key == 'Escape':
        # Prepare to exit.
        reactor.stop()
    # If the game is not over
    if reactor.game.player.health and reactor.game.opponent.health:
        # If the player is prompted to select a chip
        if reactor.game.select:
            if key == 'Return':
                # Finish the selection.
                reactor.game.select = False
                # Add the chips to the player.
                for value in reactor.game.selected:
                    reactor.game.player.chips.append(
                        reactor.game.chips[reactor.game.picked[value]]
                    )
                # Make the first selected the first used.
                reactor.game.player.chips.reverse()
                # Remove the chips from the library.
                reactor.game.selected.sort()
                offset = 0
                for value in reactor.game.selected:
                    del reactor.game.chips[reactor.game.picked[value] - offset]
                    offset += 1
            if key == 'Right':
                reactor.game.cursor(1)
            if key == 'Left':
                reactor.game.cursor(-1)
            if key == 'a' and reactor.game.equipable(reactor.game.selection):
                # Prepare to add the chip.
                reactor.game.selected.append(reactor.game.selection)
            if key == 's' and reactor.game.selected:
                # Undo the selection.
                reactor.game.selected.pop()
        else:
            if key == 'Up':
                move(reactor.game.player, rows=1)
            if key == 'Down':
                move(reactor.game.player, rows=-1)
            if key == 'Right':
                move(reactor.game.player, cols=1)
            if key == 'Left':
                move(reactor.game.player, cols=-1)
            if key == 'a' and reactor.game.player.chips:
                reactor.game.player.usechip()
            if key == 's':
                reactor.game.player.buster()
            if key == 'd':
                # Start the selection if the custom bar is full.
                if reactor.game.custombar == 10:
                    reactor.game.custom()
            if key == 'f':
                reactor.game.time()
            if key == 'c':
                reactor.game.player.charge()
    elif key == 'r':
        reactor.game.__init__()
    draw(reactor.game)

def properties(character):
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

factory = protocol.ClientFactory()
factory.protocol = GameProtocol
root = tk.Tk()
tksupport.install(root)
root.bind_all('<Key>', keypress)
root.withdraw()
reactor.connectTCP(config['ip'], 9634, factory)
reactor.run()