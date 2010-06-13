from chips.types.cannon import Chip as Parent

class Chip(Parent):
    def properties(self):
        self.name = 'HiCannon'
        self.power = 100