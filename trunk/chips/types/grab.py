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
        self.count = 0
        self.damage = 10
        self.limit = 10
        self.properties2()

    def properties2(self):
        return

    def time(self):
        if self.count != self.limit:
            self.count += 1
            if self.count != self.limit:
                return
        deactivate = True
        col = 5
        while col > 2:
            row = 0
            success = False
            breakout = False
            while row < 3:
                panel = self.owner.field[row][col]
                if panel['stolen']:
                    success = True
                    if panel['character']:
                        deactivate = False
                        breakout = True
                        break
                row += 1
            if breakout:
                break
            if success:
                deactivate = True
                if col != 3:
                    deactivate = False
                row = 0
                while row < 3:
                    self.owner.field[row][col]['stolen'] = False
                    row += 1
            col -= 1
        if deactivate:
            self.owner.deactivatechip(self, 'time')