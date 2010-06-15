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
        self.name = 'AreaGrab'
        self.type = 'normal'

    def use(self):
        col = 3
        while col < 5:
            row = 0
            success = False
            while row < 3:
                if not self.owner.field[row][col]['stolen']:
                    success = True
                    break
                row += 1
            if success:
                row = 0
                while row < 3:
                    panel = self.owner.field[row][col]
                    if not panel['stolen']:
                        if panel['character']:
                            panel['character'].hit(self.damage)
                        else:
                            panel['stolen'] = True
                            self.owner.activatechip(self, 'time')
                    row += 1
                break
            col += 1