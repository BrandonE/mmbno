from chip import Chip as Parent

class Chip(Parent):
    def next(self, chip):
        if hasattr(chip, 'power'):
            chip.power += self.plus
            return True
        return

    def properties(self):
        self.type = 'number'
        self.properties2()

    def properties2(self):
        return

    def use(self):
        return