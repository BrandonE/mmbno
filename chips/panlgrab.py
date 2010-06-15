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

class Chip(Parent):
    def properties2(self):
        self.name = 'PanlGrab'
        self.type = 'normal'

    def use(self):
        row = self.owner.field[self.owner.row]
        for key, col in enumerate(row):
            if (
                key != 5 and
                (
                    (key > 2 and not col['stolen']) or
                    (key < 3 and col['stolen'])
                )
            ):
                if col['character']:
                    col['character'].hit(self.damage)
                else:
                    col['stolen'] = True
                    self.owner.activatechip(self, 'time')
                break