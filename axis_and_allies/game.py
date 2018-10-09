import random as r
import copy

from axis_and_allies.map_generator import MapClass
from axis_and_allies import units
from axis_and_allies.buildings import Buildings as buildings


class GameManager(object):
    def __init__(self):

        self.previous_states = []

    def add_previous(self, game):
        self.previous_states.append(copy.deepcopy(game))

    def go_back(self):
        try:
            previous_state = self.previous_states.pop()
            return previous_state
        except IndexError as e:
            print(e)
            return None


class Game:
    def __init__(self, size, nations):
        self.size = size
        self.map = MapClass(size, nations)
        self.nations = nations
        self.start_player = self.nations[0]#r.choice(self.nations)
        self.current_player = self.start_player
        self.terminal = False
        self.turn = 0
        self.phase = 0
        self.purchases = dict()
        self.purchase_units = None
        self.deployable_places = None
        self.border_tiles = self.calculate_border()
        self.starting_conditions(n=2)
        self.battles = []
        self.movable_units()
        self.recruitable_list = [2, 5]


        self.history = {}

    def follow_these(self):
        '''
        Some rules. Pls.
        :return:
        '''
        print('\n\n')
        print('1. Do not change anything in the initialization phase.')
        print('2. In the purchase phase, you are ONLY allowed to purchase units. This is done with the help of game.recruit_unit')
        print('3. In the movement phase, you are ONLY allowed to move units with the help of game.move_unit')
        print('4. In the battle phase, you guessed it, you are ONLY allowed to do battling with game.do_battle')
        print('5. In the placement phase, you are ONLY allowed to place units that already is in game.purchases')
        print('\n\n')

    def what_is_allowed(self):
        '''
        This function is used to give a overview over what kind of functions that can be used in the current phase.
        '''
        allowed = [self.next_phase]
        if self.phase == 1:
            allowed += [self.recruit_unit, self.recruitable]

        elif self.phase == 2:
            allowed.append(self.move_unit)

        elif self.phase == 2.5:
            allowed += [self.do_battle, self.take_casualties]

        elif self.phase == 3:
            allowed.append(self.move_unit_friendly)

        return allowed

    def calculate_border(self):
        '''
        This function returns the border between two nations.
        :return: border_tiles, a list of the tiles.
        '''
        border_tiles = []
        for w in self.map.board:
            last = None
            for h in w:
                if last is not None:
                    if h.owner != last.owner:
                        border_tiles.append(last)
                        border_tiles.append(h)
                last = h
        return border_tiles

    def phase_0(self):
        '''
        This function does things that has to be done each round.
        1. Calculates which units that are allowed to move this round.
        2. Finds the tile(s) where one is allowed to deploy units (industry tiles)
        3. Calculates how many 'PCUs' the current player has.
        '''
        self.movable_units()
        self.deployable_places = self.find_deployable_places()
        self.purchase_units = self.calculate_purchase_units()
        self.next_phase()

    def starting_conditions(self, n):
        '''
        This function gives the starting conditions for the game.
        The parameter n decides how many of each unit type the players are given.
        This also places the industry of the two players in opposite corners.
        '''
        for tile in self.border_tiles:
            for i in range(n):
                inf_unit = units.Infantry(owner=tile.owner)
                tank_unit = units.Tank(owner=tile.owner)
                tile.units.append(inf_unit)
                tile.units.append(tank_unit)
                tank_unit.set_position(tile.cords)
                inf_unit.set_position(tile.cords)

        # All the way to the left
        tile = self.map.board[int(self.map.board.__len__() / 2) - 1][0]
        tile.constructions.append(buildings.Industry(owner=tile.owner))
        # All the way to the right
        tile = self.map.board[int(self.map.board.__len__() / 2) - 1][self.map.board.__len__() - 1]
        tile.constructions.append(buildings.Industry(owner=tile.owner))

    def rotate(self, n=1):
        return self.nations[n:] + self.nations[:n]

    def find_deployable_places(self):
        """
        This function iterates over the board, and find places where the current player has industry.
        :return: a list of deployable places
        """
        deployable_places = []
        for w in self.map.board:
            for h in w:
                if h.owner == self.current_player:
                    for const in h.constructions:
                        if isinstance(const, buildings.Industry):
                            deployable_places.append(h)

        return deployable_places

    def valid_board(self):
        """
        This function checks if the board is valid ( no battle zones, after the turn is over)
        :return:
        """
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if unit.owner != h.owner:
                        return False, h.cords
        return True, -1

    def calculate_purchase_units(self):
        """
        :return: The current players purchase_units.
        """
        purchase_units = 0
        for w in self.map.board:
            for h in w:
                if h.owner == self.current_player:
                    purchase_units += h.value
        return purchase_units

    def next_turn(self):
        self.nations = self.rotate()
        self.current_player = self.nations[0]
        if self.current_player == self.start_player:
            self.turn += 1
        self.phase = 0

        return

    def get_turn(self):
        return self.turn

    def next_phase(self):
        if self.phase == 4:
            self.next_turn()
        else:
            self.phase += 1
        return

    def get_phase(self):

        return self.phase

    def recruitable(self):
        '''
        This function is used to calculate which type of units you are allowed to recruit.
        :return: A list of the cost associated to the units.
        '''
        recruitable = []
        for unit_cost in self.recruitable_list:
            if unit_cost < self.purchase_units:
                recruitable.append(unit_cost)
        return recruitable

    def logging(self):
        if self.current_player.name not in self.history:
            self.history[self.current_player.name] = {}
        if self.turn not in self.history[self.current_player.name]:
            self.history[self.current_player.name][self.turn] = {}
        if self.phase not in self.history[self.current_player.name][self.turn]:
            self.history[self.current_player.name][self.turn][self.phase] = {}

    def recruit_unit(self, unit_id):
        """
        This function is used to purchase units.
        :param unit_id: is the id for unit
        :return: nothing. Adds the purchased unit to the purchases dict.
        """
        unit = None
        if unit_id == 0:
            unit = units.Infantry(self.current_player)
        elif unit_id == 1:
            unit = units.Tank(self.current_player)

        self.purchase_units -= unit.cost

        if self.current_player not in self.purchases:
            self.purchases[self.current_player] = []

        if unit is not None:
            self.logging()
            if 'purchases' not in self.history[self.current_player.name][self.turn][self.phase]:
                self.history[self.current_player.name][self.turn][self.phase]['purchases'] = []
            self.history[self.current_player.name][self.turn][self.phase]['purchases'].append(type(unit))
            self.purchases[self.current_player].append(unit)
        else:
            print("Invalid unit number")

    def init_turn(self):
        """
        This function is used to init the round, for each player.
        :return:
        """

        self.deployable_places = self.calculate_purchase_units()
        self.purchase_units = self.calculate_purchase_units()
        self.battles = []

    def conquer_tile(self, tile, new_owner):
        tile.owner = new_owner

    def move_unit_friendly(self, from_tile, to_tile, unit):
        '''
        This function is used to move a unit from a tile to another.
        :param from_tile: Starting tile
        :param to_tile: End tile
        :param unit: The unit that is supposed to be moved.
        :return:
        '''
        if to_tile.owner is not self.current_player:
            return False

        delta_x = abs(from_tile.cords[0] - to_tile.cords[0])
        delta_y = abs(from_tile.cords[1] - to_tile.cords[1])
        # todo add is legal function instead.
        if delta_x + delta_y <= unit.range:
            if to_tile.owner != self.current_player:
                if unit.used_steps == 0:
                    unit.set_step(unit.range)
                else:
                    unit.set_step(delta_x + delta_y)

                # If the tile you enter is empty, it is conquered.
                if len(to_tile.units) == 0:
                    self.conquer_tile(to_tile, self.current_player)
                # If not, there will be a battle there.
                elif to_tile.cords not in self.battles:
                    self.battles.append(to_tile.cords)
            else:
                # The unit has travelled the distance.
                unit.set_step(delta_y + delta_x)

            unit.set_position(to_tile.cords)
            unit.set_old_position(from_tile.cords)
            # If the unit has travelled a distance which is equal to its range.
            if unit.used_steps == unit.range:
                try:
                    self.movable.remove(unit)
                except ValueError:
                    print(ValueError.args)




            # The actual moving of the unit.
            to_tile.units.append(unit)
            from_tile.units.remove(unit)

            self.logging()
            if 'friendly_movement' not in self.history[self.current_player.name][self.turn][self.phase]:
                self.history[self.current_player.name][self.turn][self.phase]['friendly_movement'] = []
            self.history[self.current_player.name][self.turn][self.phase]['friendly_movement'].append(
                (to_tile, from_tile, unit))

        return True

    def move_unit(self, from_tile, to_tile, unit):
        '''
        This function is used to move a unit from a tile to another.
        :param from_tile: Starting tile
        :param to_tile: End tile
        :param unit: The unit that is supposed to be moved.
        :return:
        '''

        delta_x = abs(from_tile.cords[0] - to_tile.cords[0])
        delta_y = abs(from_tile.cords[1] - to_tile.cords[1])
        # todo add is legal function instead.
        if delta_x + delta_y <= unit.range:
            if to_tile.owner != self.current_player:
                if unit.used_steps == 0:
                    unit.set_step(unit.range)
                else:
                    unit.set_step(delta_x + delta_y)

                # If the tile you enter is empty, it is conquered.
                if len(to_tile.units) == 0:
                    self.conquer_tile(to_tile, self.current_player)
                # If not, there will be a battle there.
                elif to_tile.cords not in self.battles:
                    self.battles.append(to_tile.cords)
            else:
                # The unit has travelled the distance.
                unit.set_step(delta_y + delta_x)

            unit.set_position(to_tile.cords)
            unit.set_old_position(from_tile.cords)
            # If the unit has travelled a distance which is equal to its range.
            if unit.used_steps == unit.range:
                try:
                    self.movable.remove(unit)
                except ValueError:
                    print(ValueError.args)



            # The actual moving of the unit.
            to_tile.units.append(unit)
            from_tile.units.remove(unit)

            self.logging()
            if 'combat_movement' not in self.history[self.current_player.name][self.turn][self.phase]:
                self.history[self.current_player.name][self.turn][self.phase]['combat_movement'] = []
            self.history[self.current_player.name][self.turn][self.phase]['combat_movement'].append(
                (to_tile, from_tile, unit))

        return True

    def reset_all_units(self):
        """
        Used to reset the 'walked' variable on the units.
        :return:
        """
        for h in self.map.board:
            for w in h:
                for unit in w.units:
                    unit.reset()

    def find_global_max(self):
        max_unit = 0
        for w in self.map.board:
            for h in w:
                length = h.units.__len__()
                if length > max_unit:
                    max_unit = length

        return max_unit

    def get_dice(self, n=6):
        r.seed()
        return r.randint(1, n)

    def do_battle(self, cords):
        """
        This function performs a battle given a some cords.
        It starts by separating the attacking and defending units.
        Then calculates the number of hits the two must 'take'.
        The hits are calculated based on the dice roll, and the unit's success criterion.
        :param cords:
        :return:
        Two tuples, where the first one contains the attacking unit(s) (dict), and how many hits the attacker has to take.
        the second is the defender unit(s) (dict) and how many hits the defender has to take.
        """
        attacking = dict()
        defending = dict()
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.owner == self.current_player and self.map.board[cords[0]][cords[1]].owner != self.current_player:
                if unit.type not in attacking:
                    attacking[unit.type] = []
                attacking[unit.type].append(unit)
            else:
                if unit.type not in defending:
                    defending[unit.type] = []
                defending[unit.type].append(unit)
        a_hits = 0
        for key in attacking:
            for unit in attacking[key]:
                dice = self.get_dice()
                if dice <= unit.att_success:
                    a_hits += 1
        d_hits = 0
        for key in defending:
            for unit in defending[key]:
                dice = self.get_dice()
                if dice <= unit.def_success:
                    d_hits += 1

        return (attacking, d_hits), (defending, a_hits)

    def calculate_individual_units(self):
        '''
        This function is used to calculate how many units the nations has.
        :return: A dict where the nation name is the key.
        '''
        dict_of_nations = dict()
        for nation in self.nations:
            total = 0
            for w in self.map.board:
                for h in w:
                    if h.owner == nation:
                        total += len(h.units)
            dict_of_nations[nation.name] = total

        return dict_of_nations

    def calculate_units(self):
        '''
        This function is used to calculate the total amount of units in the game.
        :return: The amount.
        '''
        total = 0
        for w in self.map.board:
            for h in w:
                total += len(h.units)
        return total

    def delete_unit(self, units):
        for unit in units:
            cords = unit.get_position()
            tile = self.map.board[cords[0]][cords[1]]
            tile.units.remove(unit)
            if unit in self.movable:
                self.movable.remove(unit)
        return True

    def movable_units(self):
        '''
        This function is used to calculate how many units that are movable.
        '''
        movable = []
        for h in self.map.board:
            for w in h:
                for unit in w.units:
                    if unit.owner == self.current_player:
                        if unit.used_steps != unit.range:
                            movable.append(unit)
        self.movable = movable

    def take_casualties(self, units, choice, n):
        to_be_deleted = []
        c = 0
        if choice == 'All':
            for key in units:
                to_be_deleted += units[key]
        else:
            for unit in units[choice]:
                if c == n:
                    break
                to_be_deleted.append(unit)
                c += 1

        self.delete_unit(to_be_deleted)

    def calculate_distance_between_tiles(self, tile_1, tile_2):
        '''
        This function is used to calculate the distance between two tiles.
        :param tile_1:
        :param tile_2:
        :return:
        '''
        x, y = tile_1.cords[0], tile_1.cords[1]
        x2, y2 = tile_2.cords[0], tile_2.cords[1]

        return abs(x - x2) + abs(y - y2)

    def is_there_a_winner(self):
        '''
        This is the function used to calculate the winner of the game.
        There are two ways of winning the game.
        1. Conquer all the tiles.
        2. Have the most tiles at turn 25.
        :return: bool, and if the game is over which nation that won.
        '''
        if self.turn == 25:
            tile_dict = {}
            for w in self.map.board:
                for h in w:
                    if h.owner.name not in tile_dict:
                        tile_dict[h.owner] = 0
                    tile_dict[h.owner] += 1 /(self.size[0] * self.size[1])

            biggest = (0, None)
            for nation in tile_dict:
                if tile_dict[nation] > biggest[0]:
                    biggest = (tile_dict[nation], nation)
            return True, biggest[1]

        else:
            winner = True
            for w in self.map.board:
                for h in w:
                    if h.owner != self.current_player:
                        winner = False
            return winner, self.current_player

    def find_movable_in_tile(self, cords):
        '''
        Finds movable units in a specific tile.
        :param cords: The coordinates of the specific tile.
        :return:
        '''
        units = []
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.used_steps < unit.range:
                units.append(unit)
        return units

    def find_unit_count(self, units: dict)-> int:
        '''
        this function summerizes the number of units in a dict. i.e {'inf' : [inf, inf, inf, inf], 'tank': [tank, tank, tank, tank}
        is equal to 8.
        :param units: A dict of with units
        :return: The amount of units.
        '''
        c = 0
        for key in units:
            c += len(units[key])

        return c

    def bot(self):
        if not self.current_player.human:
            self.current_player.bot.play_bot(self)