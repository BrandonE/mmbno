from chips.types.recov import Chip as Parent

class Chip(Parent):
    def properties(self):
        self.health = 50
        self.name = 'Recov50'