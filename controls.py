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

"""Handles all of the user input."""

from game import game

def handle(key):
    if key == 'Escape':
        root.destroy()
    if game.player.health and game.opponent.health:
        if game.select:
            if key == 'Return':
                game.select = False
                for value in game.selected:
                    game.player.chips.append(game.chips[game.picked[value]])
                game.player.chips.reverse()
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
                game.selected.append(game.selection)
            if key == 's' and game.selected:
                game.selected.pop()
        else:
            if key == 't':
                game.time()
            if key == 'Up':
                game.player.move(rows=1)
            if key == 'Down':
                game.player.move(rows=-1)
            if key == 'Right':
                game.player.move(cols=1)
            if key == 'Left':
                game.player.move(cols=-1)
            if key == 'a' and game.player.chips:
                game.player.usechip()
            if key == 's':
                game.player.buster()
            if key == 'd':
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