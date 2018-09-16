import random as r


class Bot(object):
    def __init__(self):
        self.moved = dict()

    def play_bot(self, game):
        if game.phase == 0:
            self.phase_0(game)
        elif game.phase == 1:
            self.phase_1(game)
        elif game.phase == 2:
            self.phase_2(game)
        elif game.phase == 2.5:
            self.combat_phase(game)
        elif game.phase == 3:
            self.phase_3(game)
        elif game.phase == 4:
            self.phase_4(game)
        elif game.phase == 5:
            self.phase_5(game)

    def phase_0(self, game):
        game.phase_0()

    def phase_1(self, game):
        used = 0
        while True:
            pos = game.recruitable(game.purchase_units - used)
            if pos.__len__() == 0:
                game.next_phase()
                break
            choice = r.randint(0, len(pos) - 1)
            game.recruit_unit(choice)
            used += pos[choice]

    def phase_2(self, game):
        game.battles = []
        while game.movable.__len__() > 0:
            if r.random() > 0.01:
                unit = game.movable[0]
                pos = unit.get_position()
                to_tile = r.choice(game.map.board[pos[0]][pos[1]].neighbours)
                if to_tile.owner != game.current_player:
                    self.moved[to_tile.cords.__str__()] = pos
                game.move_unit(game.map.board[pos[0]][pos[1]], to_tile, 1, unit)
            else:
                break
        game.phase = 2.5

    def prioritize_casualties(self, game, values):
        to_be_deleted = dict()
        attacker_types = list(values[0].keys())
        for i in range(values[1]):
            unit_type = r.choice(attacker_types)
            unit = values[0][unit_type][0]
            if unit.type not in to_be_deleted:
                to_be_deleted[unit.type] = []
            to_be_deleted[unit.type].append(unit)
            values[0][unit_type].remove(unit)
            if len(values[0][unit_type]) == 0:
                values[0].pop(unit_type, None)
            attacker_types = list(values[0].keys())

        for key in to_be_deleted:
            game.take_casualties(to_be_deleted, to_be_deleted[key][0].type, len(to_be_deleted[key]))

        return NotImplementedError

    def combat_phase(self, game):
        while len(game.battles) > 0:
            results = game.do_battle(game.battles[0])
            attacker = results[0]
            defender = results[1]
            attack_finished = False
            defend_finished = False
            if attacker[1] > 0:
                attacker_count = game.find_unit_count(attacker[0])
                if attacker[1] >= attacker_count:
                    game.take_casualties(attacker[0], 'All', attacker_count)
                    attack_finished = True
                else:
                    game.current_player.bot.prioritize_casualties(game, attacker)
            if defender[1] > 0:
                defender_count = game.find_unit_count(defender[0])
                if defender[1] >= defender_count:
                    game.take_casualties(defender[0], 'All', defender_count)
                    defend_finished = True
                else:
                    defender_keys = list(defender[0].keys())
                    if not defender[0][defender_keys[0]][0].owner.human:
                        defender[0][defender_keys[0]][0].owner.bot.prioritize_casualties(game, defender)
                    else:
                        game.current_player = defender[0][defender_keys[0]][0].owner
                        return defender

            if defend_finished and not attack_finished:
                game.conquer_tile(game.map.board[game.battles[0][0]][game.battles[0][1]], game.current_player)

            if attack_finished or defend_finished:
                game.battles.remove(game.battles[0])
        game.phase = 3


    def phase_3(self, game):
        while len(game.movable) > 0:
            if r.random() > 0.5:
                unit = game.movable[0]
                pos = unit.get_position()
                possible = []

                for tile in game.map.board[pos[0]][pos[1]].neighbours:
                    if tile.owner == game.current_player:
                        possible.append(tile)
                if len(possible) == 0:
                    game.movable.remove(game.movable[0])
                    break
                to_tile = r.choice(possible)
                if to_tile.owner == game.current_player:
                    game.move_unit(game.map.board[pos[0]][pos[1]], to_tile, 1, unit)
            else:
                break
        game.next_phase()

    def phase_4(self, game):
        game.next_phase()

    def phase_5(self, game):
        if game.current_player in game.purchases and len(game.deployable_places) > 0:
            while len(game.purchases[game.current_player]) > 0:
                i = r.randint(0, len(game.deployable_places) - 1)
                tile = game.deployable_places[i]
                unit = game.purchases[game.current_player][0]
                game.purchases[game.current_player].remove(unit)
                tile.units.append(unit)
                unit.set_position(tile.cords)

        if game.is_there_a_winner():
            return True
        else:
            game.reset_all_units()
            if not game.valid_board()[0]:
                print("Not Valid mando")
                print(game.map.board)
            else:
                game.next_phase()


