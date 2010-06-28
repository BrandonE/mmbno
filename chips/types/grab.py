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
    def activate(self):
        """Add the chip to the active chips."""
        # Remove the old Grab active chips.
        for type in ['move', 'time']:
            discard = []
            for chip in self.owner.activechips[type]:
                if chip.name in ['AreaGrab', 'PanelGrab']:
                    discard.append(chip)
            for value in discard:
                self.owner.activechips[type].discard(chip)
        self.owner.activatechip(self, 'move')
        self.owner.activatechip(self, 'time')

    def move(self):
        """Do something after moving."""
        # If the counter has expired
        if self.count == self.limit:
            rows = len(self.owner.owner.field)
            cols = len(self.owner.owner.field[0])
            deactivate = True
            for col in range(cols - 1, (cols / 2) - 1, -1):
                success = False
                breakout = False
                for row in range(0, rows):
                    panel = self.owner.owner.field[row][col]
                    # If this panel has been stolen
                    if panel['stolen']:
                        success = True
                        # If this panel contains a character
                        if panel['character']:
                            deactivate = False
                            breakout = True
                            break
                if breakout:
                    break
                if success:
                    # If none of the stolen panels contain a character,
                    # deactivate the chips
                    if col != rows:
                        deactivate = False
                    # Restore the panels.
                    for row in range(0, rows):
                        self.owner.owner.panel(row, col, stolen=False)
            if deactivate:
                self.owner.deactivatechip(self, 'move')
                self.owner.deactivatechip(self, 'time')

    def properties(self):
        """Overwrite the default properties."""
        self.count = 0
        self.damage = 10
        self.limit = 10
        self.properties2()

    def properties2(self):
        """Overwrite the default properties."""
        return

    def time(self):
        """Handle a unit of time."""
        # Increment the counter if not expired.
        if self.count != self.limit:
            self.count += 1
        self.move()