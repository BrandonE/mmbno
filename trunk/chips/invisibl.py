from chip import Chip as Parent

class Chip(Parent):
    def hit(self, power):
        return

    def properties(self):
        self.name = 'Invisibl'

    def use(self):
        self.owner.activatechip(self, 'hit')