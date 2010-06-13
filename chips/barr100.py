from chips.types.barr import Chip as Parent

class Chip(Parent):
    def properties2(self):
        self.health = 100
        self.name = 'Barr100'