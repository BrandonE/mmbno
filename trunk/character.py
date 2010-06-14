class Character():
    def __init__(self, field, row = 1, col = 1):
        self.field = field
        self.row = row
        self.col = col
        self.activechips = {
            'death': {},
            'heal': {},
            'hit': {},
            'time': {}
        }
        self.chips = []
        self.health = 500
        self.maxhealth = self.health
        self.name = 'MegaMan.EXE'
        self.power = 1
        self.status = set()
        self.type = 'normal'
        self.properties()

    def activatechip(self, chip, type):
        if hasattr(chip, 'priority'):
            self.activechips[type][chip.priority] = chip

    def buster(self):
        self.shoot(self.power, 'normal')

    def charge(self):
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

    def defaulttime(self):
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

    def hit(self, power, type):
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
        if self.activechips['hit']:
            self.getactivechip('hit').hit(power)
            return
        self.defaulthit(power)
        self.defaultdeath()

    def move(self, rows = 0, cols = 0, force = False):
        newrow = self.row - rows
        newcol = self.col + cols
        if not force:
            if self.field[self.row][self.col]['character'] != self:
                raise Exception('Field desync!')
            if self.col > 2:
                raise Exception('Offsides!')
            if (
                newrow < 0 or
                newrow > 2 or
                (
                    (newcol < 0 or newcol > 2) and
                    self.field[newrow][newcol]['inverted'] == False
                ) or
                (
                    (newcol >= 0 or newcol <= 2) and
                    self.field[newrow][newcol]['inverted'] == True
                ) or
                not self.field[newrow][newcol]['character'] == None or
                (
                    self.field[newrow][newcol]['status'] == 'broken' and
                    not 'airshoes' in self.status
                ) or
                'paralyzed' in self.status
            ):
                return
        self.field[self.row][self.col]['character'] = None
        if (
            self.field[self.row][self.col]['status'] == 'cracked' and
            (self.row != newrow or self.col != newcol)
        ):
            self.field[self.row][self.col]['status'] = 'broken'
        self.field[newrow][newcol]['character'] = self
        self.row = newrow
        self.col = newcol

    def properties(self):
        return

    def shoot(self, power, type):
        row = self.field[self.row]
        for key, col in enumerate(row):
            if key > self.col and col['character']:
                col['character'].hit(power, type)
                break

    def time(self):
        if self.activechips['time']:
            self.getactivechip('time').time()
            return
        self.defaulttime()

    def usechip(self):
        chip = self.chips.pop()
        result = True
        while self.chips and result:
            chip2 = self.chips.pop()
            result = chip2.next(chip)
            if not result:
                self.chips.append(chip2)
        chip.use()