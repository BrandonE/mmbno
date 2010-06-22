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

from messages import move
from game import game

__all__ = ['handle']

def handle(key):
    """Handle a key press."""
    if key == 'Escape':
        # Prepare to exit.
        return True
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