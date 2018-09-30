class Nation(object):
    def __init__(self, name, human=False, bot=None):
        self.name = name
        self.human = human
        self.bot = bot

    def __repr__(self):
        return self.name
