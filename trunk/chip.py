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

class Chip():
    def __init__(self, owner, settings):
        self.owner = owner
        self.settings = settings
        self.priority = 0
        self.type = 'none'
        self.stars = 1
        self.properties()

    def dead(self):
        self.owner.defaultdead()

    def hit(self, power):
        self.owner.defaulthit(self, power)

    def heal(self, health):
        self.owner.defaultheal(self, health)

    def next(self, chip):
        return

    def properties(self):
        return

    def time(self):
        self.owner.defaulttime(self)

    def use(self):
        return