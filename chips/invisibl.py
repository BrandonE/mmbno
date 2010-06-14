from chip import Chip as Parent

class Chip(Parent):
    def hit(self, power):
        return

    def properties(self):
        self.name = 'Invisibl'
        self.count = 0
        self.limit = 10

    def time(self):
        self.count += 1
        if self.count == self.limit:
            self.owner.deactivatechip(self, 'hit')
            self.owner.deactivatechip(self, 'time')

    def use(self):
        self.owner.activatechip(self, 'hit')
        self.owner.activatechip(self, 'time')