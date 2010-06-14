from chip import Chip as Parent

class Chip(Parent):
    def properties(self):
        self.name = 'BusterUp'
        self.plus = 1
        self.type = 'number'

    def use(self):
        self.owner.power += self.plus