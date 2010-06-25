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

"""A class to base the characters off of."""

from math import ceil
from config import config
from messages import hit, move, update

__all__ = ['Character']

class Character():
    """A class to base the characters off of."""
    def __init__(self, owner, id, row = 1, col = 1):
        """A class to base the characters off of."""
        self.owner = owner
        self.id = id
        self.row = row
        self.col = col
        self.chips = []
        # Chips that modify the character temporarily.
        self.activechips = {
            'death': {},
            'heal': set([]),
            'hit': {},
            'move': set([]),
            'time': set([])
        }
        self.health = -1
        self.maxhealth = self.health
        self.name = 'Empty'
        self.power = 0
        self.status = set([])
        self.type = 'none'
        self.properties()

    def activatechip(self, chip, type):
        """Add a chip to the active chips."""
        if isinstance(self.activechips[type], dict):
            self.activechips[type][chip.priority] = chip
            return
        self.activechips[type].add(chip)

    def buster(self):
        """Use a regular buster shot."""
        if not 'paralyzed' in self.status:
            self.shoot(self.power)

    def charge(self):
        """Use a charge shot."""
        if not 'paralyzed' in self.status:
            self.shoot(self.power * 10, self.type)

    def deactivatechip(self, chip, type):
        """Remove a chip to the active chips."""
        if (
            isinstance(self.activechips[type], dict) and
            chip.priority in self.activechips[type]
        ):
            del self.activechips[type][chip.priority]
            return
        self.activechips[type].discard(chip)

    def death(self):
        """Check if the character should die."""
        # If an active chip exists, override the original handling.
        if self.activechips['death']:
            self.priority('death').death()
            return
        self.defaultdeath()
        update(self, 'character')

    def defaultdeath(self):
        """The default handling for checking if a character should die."""
        return

    def defaultheal(self, health):
        return

    def defaulthit(self, power):
        """The default handling for damage."""
        return

    def defaultmove(self, rows, cols, blue, force):
        return

    def defaultslide(self, rows, cols, blue, force):
        return

    def defaulttime(self):
        return

    def heal(self, health):
        """Heal the character."""
        self.defaultheal(health)
        # Run all of the active chip modifiers.
        converted = list(self.activechips['heal'])
        for value in converted:
            value.heal()
        update(self, 'character')

    def hit(self, power, type = 'none'):
        """Handle damage."""
        weaknesses = {
            'aqua': 'electric',
            'break': 'cursor',
            'cursor': 'wind',
            'electric': 'wood',
            'fire': 'aqua',
            'sword': 'break',
            'wind': 'sword',
            'wood': 'fire'
        }
        # Double the damage if the attack is the character's weakness.
        if self.type in weaknesses and weaknesses[self.type] == type:
            power *= 2
        weaknesses = {
            'grass': 'fire',
            'ice': 'electric'
        }
        status = self.owner.field[self.row][self.col]['status']
        # Double the damage if the attack is the panel's weakness.
        if status in weaknesses and weaknesses[status] == type:
            power *= 2
        # Half the damage if on a holy panel.
        if status == 'holy':
            power = int(ceil(power / 2))
        # If an active chip exists, override the original handling.
        if self.activechips['hit']:
            self.priority('hit').hit(power)
            update(self)
            return
        self.defaulthit(power)
        update(self, 'character')

    def move(self, rows = 0, cols = 0, blue = config['blue'], force = False):
        """Move the character if possible."""
        self.defaultmove(rows, cols, blue, force)
        # Run all of the active chip modifiers.
        converted = list(self.activechips['move'])
        for value in converted:
            value.move()
        update(self, 'character')
        self.defaultslide(rows, cols, blue, force)

    def priority(self, type):
        """Grab the active chip with the highest priority."""
        chips = self.activechips.copy()[type].copy()
        return self.activechips[type][sorted(chips).pop()]

    def properties(self):
        """Overwrite the default properties."""
        return

    def shoot(self, power, type = 'none'):
        """Hit the first person across from the character."""
        if not 'paralyzed' in self.status:
            for col in range(self.col + 1, 6):
                panel = self.owner.field[self.row][col]
                # If this panel contains a character
                if panel['character']:
                    hit(panel['character'], power, type)
                    # If the attack is a fire type and the panel has grass,
                    # burn it.
                    if panel['status'] == 'grass' and type == 'fire':
                        panel['status'] = 'normal'
                    break

    def time(self):
        """Handle a unit of time."""
        self.defaulttime()
        # Run all of the active chip modifiers.
        converted = list(self.activechips['time'])
        for value in converted:
            value.time()
        update(self, 'character')

    def update(self, **kwargs):
        self.owner.field[self.row][self.col] = None
        for key, value in kwargs.items():
            if 'key' == 'status':
                value = set(value)
            setattr(self, key, value)
        self.owner.field[self.row][self.col] = self

    def usechip(self):
        """Use the next chip or set of chips."""
        if not 'paralyzed' in self.status:
            chip = self.chips.pop()
            result = True
            # Handle the next chip if it should be used in a chain.
            while self.chips and result:
                chip2 = self.chips.pop()
                result = chip2.next(chip)
                # Put it the next chip back if it shouldn't be used in a chain.
                if not result:
                    self.chips.append(chip2)
            chip.use()