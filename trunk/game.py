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
from random import randint
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
        self.player = Character(field)
        self.player.move(0, 0, True)
        from characters.bass import Character
        self.opponent = Character(opponentfield)
        self.opponent.move(0, 0, True)
        field[0][0]['status'] = 'broken'
        field[2][0]['status'] = 'cracked'
        field[0][5]['status'] = 'broken'
        self.chips = json.loads(
            open(
                os.path.join('chips', 'folders', config['chipfolder'])
            ).read()
        )
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
            self.chips[key].code = value['code']
        self.custom()

    def cursor(self, cols):
        newcol = self.selection + cols
        if newcol >= 0 and newcol < len(self.picked):
            self.selection = newcol

    def custom(self):
        self.player.chips = []
        self.pickchips()
        self.select = True
        self.selection = 0
        self.selected = []
        self.time = 0

    def equipable(self, chip):
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

game = Game()