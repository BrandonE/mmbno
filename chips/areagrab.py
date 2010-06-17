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
        self.codes = ('B', 'F', 'S')
        self.description = 'Steals left edge from enemy'
        self.name = 'AreaGrab'
        self.stars = 2

    def use(self):
        for col in range(1, 5):
            success = False
            for row in range(0, 3):
                panel = self.owner.field[row][col]
                if (
                    (col > 2 and not panel['stolen']) or
                    (col < 3 and panel['stolen'])
                ):
                    success = True
                    break
            if success:
                for row in range(0, 3):
                    panel = self.owner.field[row][col]
                    if (
                        (col > 2 and not panel['stolen']) or
                        (col < 3 and panel['stolen'])
                    ):
                        if panel['character']:
                            panel['character'].hit(self.damage)
                        else:
                            panel['stolen'] = not panel['stolen']
                            if panel['stolen']:
                                self.owner.activatechip(self, 'move')
                                self.owner.activatechip(self, 'time')
                break