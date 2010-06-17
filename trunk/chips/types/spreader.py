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
    def use(self):
        row = self.owner.field[self.owner.row]
        for key, panel in enumerate(row):
            if key > self.owner.col and panel['character']:
                break
        top = self.owner.row - 1
        left = key - 1
        for rowoffset in range(0, 3):
            for coloffset in range(0, 3):
                row = top + rowoffset
                col = left + coloffset
                if row > -1 and row < 3 and col > -1 and col < 6:
                    panel = self.owner.field[row][col]
                    if (
                        panel['character'] and
                        (col > 2 or panel['stolen']) and
                        (col < 3 or not panel['stolen'])
                    ):
                        panel['character'].hit(self.power, self.type)