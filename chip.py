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

"""A class to base the chips off of."""

__all__ = ['Chip']

class Chip():
    """A class to base the chips off of."""
    def __init__(self, owner):
        """A class to base the chips off of."""
        self.owner = owner
        self.element = 'none'
        self.classification = 'standard'
        self.priority = 0
        self.stars = 1
        self.properties()

    def damage(self, power):
        """Handle damage."""
        self.owner.damage(self, power)

    def heal(self, health):
        """Heal the character."""
        return

    def next(self, chip):
        """Handle a chain."""
        return

    def properties(self):
        """Overwrite the default properties."""
        return

    def time(self):
        """Handle a unit of time."""
        return

    def use(self):
        """Use the chip."""
        return