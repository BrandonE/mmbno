from chips.types.barr import Chip as Parent

class Chip(Parent):
    def properties2(self):
        self.health = 10
        self.name = 'Barr10'