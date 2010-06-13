from chips.types.recov import Chip as Parent

class Chip(Parent):
    def properties(self):
        self.health = 30
        self.name = 'Recov30'