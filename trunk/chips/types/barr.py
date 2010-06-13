from chip import Chip as Parent

class Chip(Parent):
    def hit(self, power):
        self.health -= power
        if self.health <= 0:
            self.owner.deactivatechip(self, 'hit')

    def properties(self):
        self.priority = 1
        self.properties2()

    def properties2(self):
        return

    def use(self):
        self.owner.activatechip(self, 'hit')