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
from config import config
import messages

__all__ = ['Chip']

class Chip(Parent):
    """A version of the Chip class."""
    def properties(self):
        """Overwrite the default properties."""
        self.codes = ('*',)
        self.description = 'Knock enemy back 1 square'
        self.name = 'Airshot'
        self.power = 20
        self.stars = 2
        self.type = 'air'

    def use(self):
        """Use the chip."""
        for col in range(self.owner.col + 1, 6):
            panel = self.owner.owner.field[self.owner.row][col]
            # If this panel contains a character and is not yours
            if panel['character'] and (col > 2 ^ panel['stolen']):
                messages.hit(panel['character'], self.power)
                # Move it back 1.
                messages.move(
                    panel['character'],
                    cols=-1,
                    blue=(not config['blue'])
                )
                break