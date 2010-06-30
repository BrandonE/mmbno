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

"""A version of the Chip class."""

from chips.types.grab import Chip as Parent

__all__ = ['Chip']

class Chip(Parent):
    """A version of the Chip class."""
    def properties2(self):
        """Overwrite the default properties."""
        self.codes = ('B', 'F', 'S')
        self.description = 'Steals left edge from enemy'
        self.name = 'AreaGrab'
        self.stars = 2

    def use(self):
        """Use the chip."""
        cols = len(self.owner.owner.field[0])
        breakout = False
        for col in range(1, cols - 1):
            for row in range(0, len(self.owner.owner.field)):
                panel = self.owner.owner.field[row][col]
                # If this panel is not on this side
                if (col > (cols / 2) - 1) ^ panel['stolen']:
                    # If this panel contains a character
                    if panel['character']:
                        self.owner.owner.hit(row, col, self.damage)
                    else:
                        # Take it.
                        self.owner.owner.panel(
                            row,
                            col,
                            stolen=not panel['stolen']
                        )
                        if not panel['stolen']:
                            self.activate()
                    # Stop running through the columns.
                    breakout = True
            if breakout:
                break