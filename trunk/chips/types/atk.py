from chip import Chip as Parent

class Chip(Parent):
    def next(self, chip):
        if hasattr(chip, 'power'):
            chip.power += self.plus
            return True
        return

    def use(self):
        return