from chips.types.atk import Chip as Parent

class Chip(Parent):
    def properties2(self):
        self.name = 'Atk+10'
        self.plus = 10