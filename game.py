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

    def pickchips(self):
        picked = set([])
        while len(self.chips) != len(picked) and len(picked) < 10:
            picked.add(randint(0, len(self.chips) - 1))
        self.picked = list(picked)

game = Game()