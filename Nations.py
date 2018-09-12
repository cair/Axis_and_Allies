class Nation(object):
    def __init__(self, name, human=True, difficulty="Random", bot=None):
        self.name = name
        self.human = human
        self.difficulty = None
        if not self.human:
            self.difficulty = difficulty
        self.bot = bot

    def __repr__(self):
        return self.name
