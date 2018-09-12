class Nation(object):
    def __init__(self, name, human=True, difficulty="Random"):
        self.name = name
        self.human = human
        self.difficulty = None
        if not self.human:
            self.difficulty = difficulty

    def __repr__(self):
        return self.name
