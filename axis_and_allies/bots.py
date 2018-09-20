import random as r


def random_bot(self):
    moved = dict()
    if self.phase == 0:
        self.phase_0()
    elif self.phase == 1:
        used = 0
        while True:
            pos = self.recruitable(self.purchase_units - used)
            if pos.__len__() == 0:
                self.next_phase()
                break
            choice = r.randint(0, len(pos) - 1)
            self.recruit_unit(choice)
            used += pos[choice]
    elif self.phase == 2:
        self.battles = []
        while self.movable.__len__() > 0:
            if r.random() > 0.01:
                unit = self.movable[0]
                pos = unit.get_position()
                to_tile = r.choice(self.map.board[pos[0]][pos[1]].neighbours)
                if to_tile.owner != self.current_player:
                    moved[to_tile.cords.__str__()] = pos
                self.move_unit(self.map.board[pos[0]][pos[1]], to_tile, 1, unit)
            else:
                break
        self.phase = 2.5
    elif self.phase == 2.5:
        while self.battles.__len__() > 0:
            results = self.do_battle(self.battles[0])
            attacker = results[0]
            defender = results[1]
            attack_finished = False
            defend_finished = False
            if attacker[1] > 0:
                attacker_count = self.find_unit_count(attacker[0])
                attacker_types = list(attacker[0].keys())
                if attacker[1] >= attacker_count:
                    self.take_casualties(attacker[0], 'All', attacker_count)
                    attack_finished = True
                else:
                    to_be_deleted = dict()
                    for i in range(attacker[1]):
                        unit_type = r.choice(attacker_types)
                        unit = attacker[0][unit_type][0]
                        if unit.type not in to_be_deleted:
                            to_be_deleted[unit.type] = []
                        to_be_deleted[unit.type].append(unit)
                        attacker[0][unit_type].remove(unit)
                        if attacker[0][unit_type].__len__() == 0:
                            attacker[0].pop(unit_type, None)
                        attacker_types = list(attacker[0].keys())

                    for key in to_be_deleted:
                        self.take_casualties(to_be_deleted, to_be_deleted[key][0].type, to_be_deleted[key].__len__())

            if defender[1] > 0:
                defender_count = self.find_unit_count(defender[0])
                defender_types = list(defender[0].keys())
                if defender[1] >= defender_count:
                    self.take_casualties(defender[0], 'All', defender_count)
                    defend_finished = True
                else:
                    defender_keys = list(defender[0].keys())
                    if not defender[0][defender_keys[0]][0].owner.human:
                        to_be_deleted = dict()
                        for i in range(defender[1]):
                            unit_type = r.choice(defender_types)
                            unit = defender[0][unit_type][0]
                            if unit.type not in to_be_deleted:
                                to_be_deleted[unit.type] = []
                            to_be_deleted[unit.type].append(unit)
                            defender[0][unit_type].remove(unit)
                            if defender[0][unit_type].__len__() == 0:
                                defender[0].pop(unit_type, None)
                            defender_types = list(defender[0].keys())
                        for key in to_be_deleted:
                            self.take_casualties(to_be_deleted, to_be_deleted[key][0].type,
                                                 to_be_deleted[key].__len__())
                    else:
                        self.current_player = defender[0][defender_keys[0]][0].owner
                        return defender

            if defend_finished and not attack_finished:
                self.conquer_tile(self.map.board[self.battles[0][0]][self.battles[0][1]], self.current_player)

            if attack_finished or defend_finished:
                self.battles.remove(self.battles[0])

        self.phase = 3
    elif self.phase == 3:
        while self.movable.__len__() > 0:
            if r.random() > 0.5:
                unit = self.movable[0]
                pos = unit.get_position()
                possible = []

                for tile in self.map.board[pos[0]][pos[1]].neighbours:
                    if tile.owner == self.current_player:
                        possible.append(tile)
                if possible.__len__() == 0:
                    self.movable.remove(self.movable[0])
                    break
                to_tile = r.choice(possible)
                if to_tile.owner == self.current_player:
                    self.move_unit(self.map.board[pos[0]][pos[1]], to_tile, 1, unit)
            else:
                break
        self.next_phase()
    elif self.phase == 4:
        self.next_phase()
    elif self.phase == 5:
        if self.current_player in self.purchases and self.deployable_places.__len__() > 0:
            while self.purchases[self.current_player].__len__() > 0:
                i = r.randint(0, self.deployable_places.__len__() - 1)
                tile = self.deployable_places[i]
                unit = self.purchases[self.current_player][0]
                self.purchases[self.current_player].remove(unit)
                tile.units.append(unit)
                unit.set_position(tile.cords)

        if self.is_there_a_winner():
            return True
        else:
            self.reset_all_units()
            if not self.valid_board()[0]:
                print("Not Valid mando")
                print(self.map.board)
            self.next_phase()
