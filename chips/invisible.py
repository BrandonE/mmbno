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
    def properties(self):
        """Overwrite the default properties."""
        self.codes = ('*',)
        self.count = 0
        self.description = 'Invisible for a while'
        self.limit = 10
        self.name = 'Invisible'
        self.stars = 3

    def time(self):
        """Handle a unit of time."""
        self.count += 1
        # Increment the counter if not expired.
        if self.count == self.limit:
            self.owner.deactivatechip(self, 'damage')
            self.owner.deactivatechip(self, 'time')

    def use(self):
        """Use the chip."""
        self.owner.activatechip(self, 'damage')
        self.owner.activatechip(self, 'time')