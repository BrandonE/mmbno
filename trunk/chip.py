class Chip():
    def __init__(self, owner, settings):
        self.owner = owner
        self.settings = settings
        self.priority = 0
        self.properties()

    def buster(self):
        self.owner.defaultbuster()

    def dead(self):
        self.owner.defaultdead()

    def hit(self, power):
        self.owner.defaulthit(self)

    def next(self, chip):
        return

    def properties(self):
        return

    def use(self):
        return