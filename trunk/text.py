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

"""Creates the text representation of the game."""

import os
import Tkinter as tk
from game import game
from controls import handle

status = {
    'air': 'A',
    'none': 'N',
    'plus': 'P'
}

def chardraw(character):
    print '\n%s' % (character.name)
    print '-HP: %s' % (str(character.health))
    print '-Status: %s' % (', '.join(character.status))
    print '-Type: %s' % (character.type)
    chips = []
    for value in character.chips:
        power = ''
        if hasattr(value, 'power'):
            power = ' %s' % (value.power)
        chips.append('%s%s %s' % (value.name, power, status[value.type]))
    print '-Chips: %s' % (', '.join(chips))
    print '-Active Chip:'
    for key, type in character.activechips.items():
        if type:
            names = []
            if isinstance(type, dict):
                type = list(dict([(v, k) for (k, v) in type.iteritems()]))
            for chip in type:
                names.append(chip.name)
            print '--%s: %s' % (key, ', '.join(names))

def draw():
    os.system('cls')
    if game.select:
        menu = ''
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
                    status[game.chips[chip].type],
                    game.chips[chip].code,
                    equipable
                )
            else:
                menu += '%s%s %s %s %s' % (
                    ' ' * len(game.chips[chip].name),
                    ' ' * len(str(power)),
                    ' ' * len(status[game.chips[chip].type]),
                    ' ' * len(game.chips[chip].code),
                    ' ' * len(equipable)
                )
        print '%s|' % (menu)
    custom = ''
    if game.custombar >= 10:
        custom = ' Custom'
    print '%s%s' % (('*' * game.custombar), custom)
    fielddraw(game.player)
    fielddraw(game.opponent)
    chardraw(game.player)
    chardraw(game.opponent)
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
    print 'A: Use / Select Chip'
    print 'S: Use Buster / Remove Chip'
    print 'D: Prompt Chip Selection'
    print 'C: Charge Shot'
    print 'T: Advance time (Test)'
    print 'F: Deal 25 damage to player (Test)'
    print 'G: Deal 100 damage to player (Test)'
    print 'Enter: End Chip Selection'
    print 'Escape - End Game'

def fielddraw(character):
    grid = ''
    for row in character.field:
        grid += '\n ----- ----- ----- ----- ----- -----'
        grid += '\n|'
        for key, col in enumerate(row):
            label = ' '
            red = ' '
            panelstatus = {
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
            if col['character'] and col['character'].health:
                label = 'x'
                if character == col['character']:
                    label = 'o'
            if (key > 2 and not col['stolen']) or (key < 3 and col['stolen']):
                red = 'R'
            grid += ' %s%s%s |' % (panelstatus[col['status']], label, red)
        grid += '\n ----- ----- ----- ----- ----- -----'
    print grid

def keypress(event):
    key = event.keysym
    handle(key)
    draw()

draw()
root = tk.Tk()
root.bind_all('<Key>', keypress)
root.withdraw()
root.mainloop()