import random as r

from axis_and_allies.game import Game


class Bot(object):
    def __init__(self):
        self.moved = dict()

    def play_bot(self, game: Game):
        '''
        This is the function that executes the different actions of the bot.
        :param game: Is the object of the game that contains the map, units etc..
        :return:
        '''
        if game.phase == 0:
            self.initialization_phase(game)
        elif game.phase == 1:
            self.purchase_phase(game)
        elif game.phase == 2:
            self.moving_phase(game)
        elif game.phase == 2.5:
            self.combat_phase(game)
        elif game.phase == 3:
            self.non_combat_movement_phase(game)
        elif game.phase == 4:
            self.unit_placement_phase(game)

    def initialization_phase(self, game: Game):
        '''
        Prepares for the turn. Read the docstring @phase_0()
        :param game: Is the object of the game that contains the map, units etc..
        '''
        game.phase_0()

    def purchase_phase(self, game: Game):
        '''
        In this phase, one should only buy units. The purchased units are placed into game.purchases.
        :param game: Is the object of the game that contains the map, units etc..
        '''
        used = 0
        while True:
            possible = game.recruitable(game.purchase_units - used)
            if len(possible) == 0:
                game.next_phase()
                break
            choice = r.randint(0, len(possible) - 1)
            game.recruit_unit(choice)
            used += possible[choice]

    def moving_phase(self, game: Game):
        '''
        This is the phase where one is supposed to move units, in friendly and unfriendly territory.
        If the unit is moved to a unfriendly tile, it will become a battle zone.
        The units are moved with the function game.move_unit(from_tile, to_tile, unit)
        :param game: Is the object of the game that contains the map, units etc..
        '''
        game.battles = []
        while len(game.movable) > 0:
            if r.random() > 0.01:
                unit = game.movable[0]
                pos = unit.get_position()
                to_tile = r.choice(game.map.board[pos[0]][pos[1]].neighbours)
                if to_tile.owner != game.current_player:
                    self.moved[to_tile.cords.__str__()] = pos
                game.move_unit(game.map.board[pos[0]][pos[1]], to_tile, unit)
            else:
                break
        game.phase = 2.5

    def prioritize_casualties(self, game: Game, values: tuple)->None:
        '''
        This function is used to randomly pick units to delete after a battle.
        After the units has been selected they are deleted by the use of game.take_casualties().
        :param game: Is the object of the game that contains the map, units etc..
        :param values: A tuple with units (dict), hit counter.
        '''
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

    def combat_phase(self, game: Game) -> None:
        '''
        This is the function thas performs the battle. It starts by picking a battle from the list of battles.
        This is done by using the function game.do_battle(battle_cords). (read that doc string if in doubt)
        :param game: Is the object of the game that contains the map, units etc..
        :return:
        '''
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

    def non_combat_movement_phase(self, game: Game)-> None:
        '''
        This is the function used in the non-combat phase. In this phase it is only allowed to move units in tiles
        that the current player own.
        The units are moved with the function game.move_unit(from_tile, to_tile, unit)

        This is just an example of how movement can be implemented.
        :param game: Is the object of the game that contains the map, units etc..
        '''
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
                    game.move_unit(game.map.board[pos[0]][pos[1]], to_tile, unit)
            else:
                break
        game.next_phase()

    def unit_placement_phase(self, game: Game)-> None:
        '''
        This is the phase where one is to place the units purchased in the purchasing phase.
        One is only allowed to place units in a tile where there is industry.

        This functions randomly distributes the units.
        :param game: Is the object of the game that contains the map, units etc..

        '''
        if game.current_player in game.purchases and len(game.deployable_places) > 0:
            while len(game.purchases[game.current_player]) > 0:
                i = r.randint(0, len(game.deployable_places) - 1)
                tile = game.deployable_places[i]
                unit = game.purchases[game.current_player][0]
                game.purchases[game.current_player].remove(unit)
                tile.units.append(unit)
                unit.set_position(tile.cords)

        if game.is_there_a_winner()[0]:
            return True
        else:
            game.reset_all_units()
            if not game.valid_board()[0]:
                print(game.map.board)
            else:
                game.next_phase()
