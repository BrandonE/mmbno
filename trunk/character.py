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

class Character():
    def __init__(self, owner, field, row = 1, col = 1):
        self.owner = owner
        self.field = field
        self.row = row
        self.col = col
        self.activechips = {
            'death': {},
            'heal': {},
            'hit': {},
            'move': {},
            'time': {}
        }
        self.chips = []
        self.health = 500
        self.maxhealth = self.health
        self.name = 'MegaMan.EXE'
        self.power = 1
        self.status = set([])
        self.type = 'none'
        self.properties()

    def activatechip(self, chip, type):
        if hasattr(chip, 'priority'):
            self.activechips[type][chip.priority] = chip

    def buster(self):
        if not 'paralyzed' in self.status:
            self.shoot(self.power)

    def charge(self):
        if not 'paralyzed' in self.status:
            self.shoot(self.power * 10, self.type)

    def deactivatechip(self, chip, type):
        if hasattr(chip, 'priority'):
            del self.activechips[type][chip.priority]

    def death(self):
        if self.activechips['death']:
            self.getactivechip('death').dead()
            return
        self.defaultdeath()

    def die(self):
        return

    def defaultdeath(self):
        if self.health <= 0:
            self.health = 0
            self.die()

    def defaultheal(self, health):
        self.health += health
        if self.health > self.maxhealth:
            self.health = self.maxhealth

    def defaulthit(self, power):
        self.health -= power

    def defaultmove(self, rows = 0, cols = 0, force = False):
        panel = self.field[self.row][self.col]
        newrow = self.row - rows
        newcol = self.col + cols
        if not force:
            if newrow < 0 or newrow > 2 or newcol < 0:
                return
        newpanel = self.field[newrow][newcol]
        if not force:
            if panel['character'] != self:
                raise Exception('Field desync')
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
        panel['character'] = None
        newpanel['character'] = self
        self.row = newrow
        self.col = newcol
        if not 'floatshoes' in self.status:
            if (
                panel['status'] == 'cracked' and
                (self.row != newrow or self.col != newcol)
            ):
                panel['status'] = 'broken'
            if newpanel['status'] == 'lava' and self.type != 'fire':
                self.hit(10, 'fire')
                newpanel['status'] = 'normal'
            if newpanel['status'] == 'ice':
                self.move(rows, cols)

    def defaulttime(self):
        panel = self.field[self.row][self.col]
        if panel['status'] == 'grass' and self.type == 'wood':
            self.heal(1)
        if panel['status'] == 'poison' and not 'floatshoes' in self.status:
            self.hit(1)
        return

    def getactivechip(self, type):
        activated = self.activechips.copy()
        activated[type] = activated[type].copy()
        return self.activechips[type][sorted(activated[type]).pop()]

    def heal(self, health):
        if self.activechips['heal']:
            self.getactivechip('heal').heal(health)
            return
        self.defaultheal(health)

    def hit(self, power, type = 'none'):
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
        if self.type in weaknesses and weaknesses[self.type] == type:
            power *= 2
        weaknesses = {
            'grass': 'fire',
            'ice': 'electric'
        }
        status = self.field[self.row][self.col]['status']
        if status in weaknesses and weaknesses[status] == type:
            power *= 2
        if status == 'holy':
            power = int(ceil(power / 2))
        if self.activechips['hit']:
            self.getactivechip('hit').hit(power)
            return
        self.defaulthit(power)
        self.defaultdeath()

    def move(self, rows = 0, cols = 0, force = False):
        if self.activechips['move']:
            self.getactivechip('move').move(rows, cols, force)
            return
        self.defaultmove(rows, cols, force)

    def properties(self):
        return

    def shoot(self, power, type = 'none'):
        row = self.field[self.row]
        for key, col in enumerate(row):
            if key > self.col and col['character']:
                col['character'].hit(power, type)
                if col['status'] == 'grass' and type == 'fire':
                    col['status'] = 'normal'
                break

    def time(self):
        if self.activechips['time']:
            self.getactivechip('time').time()
            return
        self.defaulttime()

    def usechip(self):
        if not 'paralyzed' in self.status:
            chip = self.chips.pop()
            result = True
            while self.chips and result:
                chip2 = self.chips.pop()
                result = chip2.next(chip)
                if not result:
                    self.chips.append(chip2)
            chip.use()