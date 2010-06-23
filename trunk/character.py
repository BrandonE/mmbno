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
import messages

__all__ = ['Character', 'config']

class Character():
    """A class to base the characters off of."""
    def __init__(self, owner, row = 1, col = 1):
        """A class to base the characters off of."""
        self.owner = owner
        self.row = row
        self.col = col
        # Chips that modify the character temporarily.
        self.activechips = {
            'death': {},
            'heal': set([]),
            'hit': {},
            'move': set([]),
            'time': set([])
        }
        self.chips = []
        # Default to MegaMan.EXE's properties.
        self.health = 500
        self.maxhealth = self.health
        self.name = 'MegaMan.EXE'
        self.power = 1
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
        self.shoot(self.power)

    def charge(self):
        """Use a charge shot."""
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

    def die(self):
        """Handle death."""
        self.health = 0

    def defaultdeath(self):
        """The default handling for checking if a character should die."""
        if self.health <= 0:
            self.die()

    def defaulthit(self, power):
        """The default handling for damage."""
        self.health -= power
        self.death()

    def heal(self, health):
        """Heal the character."""
        self.health += health
        if self.health > self.maxhealth:
            self.health = self.maxhealth
        # Run all of the active chip modifiers.
        converted = list(self.activechips['heal'])
        for value in converted:
            value.heal()

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
            return
        self.defaulthit(power)

    def move(self, rows, cols, force):
        """Move the character if possible."""
        # Grab the panel the character is on.
        panel = self.owner.field[self.row][self.col]
        # Define the new coordinates.
        newrow = self.row - rows
        newcol = self.col + cols
        if not force:
            # If the new coordinates aren't on the field, fail.
            if newrow < 0 or newrow > 2 or newcol < 0 or newcol > 5:
                return
        # As the coordinates are valid, grab the new panel.
        newpanel = self.owner.field[newrow][newcol]
        if not force:
            # If the panel doesn't contain the character, something went
            # horribly wrong.
            if panel['character'] != self:
                raise Exception('Field desync')
            # If the new panel is out of bounds, contains a character, is
            # broken without the character having airshoes, or the character is
            # paralyzed, fail.
            if (
                (
                    newcol > 2 and
                    not newpanel['stolen']
                ) or
                (
                    newcol < 3 and
                    newpanel['stolen']
                ) or
                newpanel['character'] or
                (
                    newpanel['status'] == 'broken' and
                    not 'airshoes' in self.status
                ) or
                'paralyzed' in self.status
            ):
                return
        # Empty the old panel.
        panel['character'] = None
        # Add the character to the new panel.
        newpanel['character'] = self
        if not 'floatshoes' in self.status:
            # If the panel is cracked and the character moved, break it.
            if (
                panel['status'] == 'cracked' and
                (self.row != newrow or self.col != newcol)
            ):
                panel['status'] = 'broken'
            # If the character moved onto a lava panel and is not a fire type
            if newpanel['status'] == 'lava' and self.type != 'fire':
                self.hit(10, 'fire')
                # Revert the panel.
                newpanel['status'] = 'normal'
        # Adjust to the new coordinates.
        self.row = newrow
        self.col = newcol
        # Run all of the active chip modifiers.
        converted = list(self.activechips['move'])
        for value in converted:
            value.move()
        if not 'floatshoes' in self.status:
            # Slide if on ice.
            if newpanel['status'] == 'ice':
                messages.move(self, rows, cols)

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
                    panel['character'].hit(power, type)
                    # If the attack is a fire type and the panel has grass,
                    # burn it.
                    if panel['status'] == 'grass' and type == 'fire':
                        panel['status'] = 'normal'
                    break

    def time(self):
        """Handle a unit of time."""
        panel = self.owner.field[self.row][self.col]
        # If the character is on a grass panel and is a wood type
        if panel['status'] == 'grass' and self.type == 'wood':
            self.heal(1)
        # If the character is on a poison panel and does not have floatshoes
        # activated
        if panel['status'] == 'poison' and not 'floatshoes' in self.status:
            self.hit(1)
        # Run all of the active chip modifiers.
        converted = list(self.activechips['time'])
        for value in converted:
            value.time()

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