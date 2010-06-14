from chip import Chip as Parent

class Chip(Parent):
    def use(self):
        self.owner.shoot(self.power, self.type)