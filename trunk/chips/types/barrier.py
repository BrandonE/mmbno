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
    def hit(self, power):
        """Handle damage."""
        self.health -= power
        if self.health <= 0:
            self.owner.deactivatechip(self, 'hit')

    def properties(self):
        """Overwrite the default properties."""
        self.priority = 1
        self.properties2()

    def properties2(self):
        """Overwrite the default properties."""
        return

    def use(self):
        """Use the chip."""
        self.owner.activatechip(self, 'hit')