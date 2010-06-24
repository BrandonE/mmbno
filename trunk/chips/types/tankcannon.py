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
        for col in range(self.owner.col + 1, 6):
            panel = self.owner.owner.field[self.owner.row][col]
            # If this panel contains a character
            if panel['character']:
                panel['character'].hit(self.power, self.type)
                return
        top = self.owner.row - 1
        for rowoffset in range(0, 3):
            # Offset the row to spread to the panel on the top and bottom.
            row = top + rowoffset
            # If the offsetted row is on the field.
            if row > -1 and row < 3:
                panel = self.owner.owner.field[row][5]
                # If this panel contains a character
                if panel['character']:
                    panel['character'].hit(self.power, self.type)
                # If the panel is cracked, break it.
                if panel['status'] == 'cracked':
                    panel['status'] = 'broken'
                else:
                    # Crack it.
                    panel['status'] = 'cracked'