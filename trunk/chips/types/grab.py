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
    def move(self, rows, cols, force):
        self.owner.defaultmove(rows, cols, force)
        if self.count == self.limit:
            deactivate = True
            for col in range(5, 2, -1):
                success = False
                breakout = False
                for row in range(0, 3):
                    panel = self.owner.field[row][col]
                    if panel['stolen']:
                        success = True
                        if panel['character']:
                            deactivate = False
                            breakout = True
                            break
                if breakout:
                    break
                if success:
                    deactivate = True
                    if col != 3:
                        deactivate = False
                    for row in range(0, 3):
                        self.owner.field[row][col]['stolen'] = False
            if deactivate:
                self.owner.deactivatechip(self, 'move')
                self.owner.deactivatechip(self, 'time')

    def properties(self):
        self.count = 0
        self.damage = 10
        self.limit = 10
        self.properties2()

    def properties2(self):
        return

    def time(self):
        self.owner.defaulttime()
        if self.count != self.limit:
            self.count += 1