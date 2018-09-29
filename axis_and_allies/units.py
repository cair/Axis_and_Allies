
class Unit:
    def __init__(self, success=1):
        self.success = success
        self.position = None
        self.used_steps = 0
        self.old_position = None

    def get_old_position(self):

        return self.old_position

    def set_old_position(self, pos):

        self.old_position = pos

    def get_position(self):

        return self.position

    def set_position(self, position):
        try:
            self.position = position
            return True
        except:
            return False

    def set_step(self, increment):

        self.used_steps += increment

    def reset(self):
        self.used_steps = 0


class Infantry(Unit):
    def __init__(self, owner, success=2):
        super().__init__()
        self.range = 1
        self.owner = owner
        self.type = 'Inf'
        self.att_success = success - 1
        self.def_success = success
        self.attachment = []

        self.cost = 2

    def __repr__(self):
        pos = self.get_position()

        return self.owner.name + "_" + self.type+"_"+str(pos[0])+","+str(pos[1])


class Tank(Unit):
    def __init__(self, owner, success=3):
        super().__init__()
        self.range = 2
        self.type = 'Tank'
        self.owner = owner
        self.att_success = success
        self.def_success = success-2
        self.cost = 5

    def __repr__(self):
        pos = self.get_position()

        return self.owner.name + "_" + self.type+"_"+str(pos[0])+","+str(pos[1])