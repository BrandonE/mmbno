class Chip():
    def __init__(self, owner, settings):
        self.owner = owner
        self.settings = settings
        self.priority = 0
        self.type = 'normal'
        self.properties()

    def dead(self):
        self.owner.defaultdead()

    def hit(self, power):
        self.owner.defaulthit(self, power)

    def heal(self, health):
        self.owner.defaultheal(self, health)

    def next(self, chip):
        return

    def properties(self):
        return

    def time(self):
        self.owner.defaulttime(self)

    def use(self):
        return