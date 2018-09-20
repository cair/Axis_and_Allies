class Tile(object):
    def __init__(self, cords, name='nameless', water=False):
        self.owner = None

        self.neighbours = []

        self.cords = cords

        self.units = []

        self.constructions = []

        self.water = water

        self.value = 2

    def __repr__(self):
        return self.owner.name+self.units.__str__()+self.constructions.__str__()