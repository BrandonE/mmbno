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

"""Contains the game's data."""

import os
from random import randint, shuffle
try:
    import simplejson as json
except ImportError:
    import json
from field import flipfield, makefield

config = json.loads(open('config.json').read())

class Game():
    def __init__(self):
        field = makefield()
        opponentfield = flipfield(field)
        from characters.mega import Character
        self.player = Character(self, field)
        self.player.move(0, 0, True)
        from characters.bass import Character
        self.opponent = Character(self, opponentfield)
        self.opponent.move(0, 0, True)
        field[0][0]['status'] = 'broken'
        field[0][1]['status'] = 'grass'
        field[0][2]['status'] = 'poison'
        field[0][5]['status'] = 'broken'
        field[1][0]['status'] = 'cracked'
        field[1][1]['status'] = 'ice'
        field[1][2]['status'] = 'holy'
        field[2][0]['status'] = 'lava'
        field[1][4]['status'] = 'grass'
        self.chips = json.loads(
            open(
                os.path.join('chips', 'folders', config['chipfolder'])
            ).read()
        )
        if len(self.chips) > 30:
            raise Exception('Too many chips')
        if len(self.chips) < 30:
            raise Exception('Too few chips')
        self.chips = self.chips[0:30]
        for key, value in enumerate(self.chips):
            module = __import__(
                'chips.%s' % (value['chip']),
                globals(),
                locals(),
                ('Chip',),
                -1
            )
            self.chips[key] = module.Chip(self.player, value)
            if not value['code'] in self.chips[key].codes:
                raise Exception('Improper chip code')
            self.chips[key].code = value['code']
        self.custom()

    def cursor(self, cols):
        newcol = self.selection + cols
        if newcol >= 0 and newcol < len(self.picked):
            self.selection = newcol

    def custom(self):
        self.custombar = 0
        self.player.chips = []
        self.pickchips()
        self.select = True
        self.selection = 0
        self.selected = []

    def equipable(self, chip):
        if (
            self.selection in self.selected or
            len(self.selected) > 4 and
            self.selection > len(self.chips) - 1
        ):
            return False
        self.selected.append(chip)
        chip = game.chips[game.picked[chip]]
        chips = set([])
        codes = set([])
        success = True
        for value in self.selected:
            thischip = self.chips[self.picked[value]]
            if thischip.code != '*':
                codes.add(thischip.code)
            chips.add(thischip.name)
            if len(chips) > 1 and len(codes) > 1:
                success = False
                break
        self.selected.pop()
        return success

    def pickchips(self):
        picked = set([])
        while len(self.chips) != len(picked) and len(picked) < 10:
            picked.add(randint(0, len(self.chips) - 1))
        self.picked = list(picked)
        shuffle(self.picked)

    def time(self):
        if self.custombar != 10:
            self.custombar += 1
        for key, row in enumerate(self.player.field):
            for key2, col in enumerate(row):
                if col['status'] == 'broken':
                    self.player.field[key][key2]['time'] += 1
                    if col['time'] == 10:
                        self.player.field[key][key2]['status'] = 'normal'
                        self.player.field[key][key2]['time'] = 0
        self.player.time()
        self.opponent.time()

game = Game()