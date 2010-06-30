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

from chip import Chip as Parent

__all__ = ['Chip']

class Chip(Parent):
    """A version of the Chip class."""
    def use(self):
        """Use the chip."""
        row = self.owner.row
        rows = len(self.owner.owner.field)
        cols = len(self.owner.owner.field[0])
        for col in range(self.owner.col + 1, cols):
            panel = self.owner.owner.field[row][col]
            # If this panel contains a character and is not on this side
            if (
                panel['character'] and
                ((col > (cols / 2) - 1) ^ panel['stolen'])
            ):
                self.owner.owner.hit(row, col, self.power, self.type)
                return
        top = self.owner.row - 1
        for rowoffset in range(0, 3):
            # Offset the row to spread to the panel on the top and bottom.
            row = top + rowoffset
            # If the offsetted row is on the field.
            if row > -1 and row < rows:
                panel = self.owner.owner.field[row][cols - 1]
                # If this panel contains a character
                if panel['character']:
                    self.owner.owner.hit(row, cols - 1, self.power, self.type)
                # If the panel is cracked, break it.
                if panel['status'] == 'cracked':
                    panel['status'] = 'broken'
                    self.owner.owner.panel(row, cols - 1, status='broken')
                else:
                    # Crack it.
                    self.owner.owner.panel(row, cols - 1, status='cracked')