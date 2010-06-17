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

class Chip(Parent):
    def properties(self):
        self.codes = ('*')
        self.description = 'Knock enemy back 1 square'
        self.name = 'Airshot'
        self.power = 20
        self.stars = 2
        self.type = 'air'

    def use(self):
        self.owner.shoot(self.power, self.type)
        for key, panel in enumerate(self.owner.field[self.owner.row]):
            if key > self.owner.col and panel['character']:
                panel['character'].move(cols=-1)
                break