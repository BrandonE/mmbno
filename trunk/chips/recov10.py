from chips.types.recov import Chip as Parent

class Chip(Parent):
    def properties(self):
        self.health = 10
        self.name = 'Recov10'