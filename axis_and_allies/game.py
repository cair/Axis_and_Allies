import random as r
import copy

from axis_and_allies.map_generator import MapClass
from axis_and_allies import units
from axis_and_allies.buildings import Buildings as buildings

class GameManager(object):
    def __init__(self):

        self.previous_states = []

    def add_previous(self, game):
        print("Legger til forrige")
        self.previous_states.append(copy.deepcopy(game))

    def go_back(self):
        try:
            print("Går tilbake til forrige")
            previous_state = self.previous_states.pop()
            return previous_state
        except IndexError as e:
            print(e)
            return None


class Game():
    def __init__(self, size, nations):
        self.map = MapClass(size, nations)
        self.nations = nations
        self.start_player = nations[0]
        self.current_player = self.start_player
        self.terminal = False
        self.turn = 0
        self.phase = 0
        self.purchases = dict()
        self.purchase_units = None  # self.calculate_purchase_units()
        self.deployable_places = None
        self.border_tiles = self.calculate_border()
        self.starting_conditions(n=2)
        self.battles = []
        self.movable_units()
        self.recruitable_list = [2, 5]
        self.history = []

    def calculate_border(self):
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
        self.movable_units()
        self.deployable_places = self.find_deployable_places()
        self.next_phase()
        self.purchase_units = self.calculate_purchase_units()

    def starting_conditions(self, n):
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
        print(self.map.board.__len__())
        # All the way to the right
        tile = self.map.board[int(self.map.board.__len__() / 2) - 1][self.map.board.__len__() - 1]
        tile.constructions.append(buildings.Industry(owner=tile.owner))

    def rotate(self, n=1):
        return self.nations[n:] + self.nations[:n]

    def find_deployable_places(self):
        deployable_places = []
        for w in self.map.board:
            for h in w:
                if h.owner == self.current_player:
                    for const in h.constructions:
                        if isinstance(const, buildings.Industry):
                            deployable_places.append(h)

        return deployable_places

    def valid_board(self):
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if unit.owner != h.owner:
                        return False, h.cords
        return True, -1

    def calculate_purchase_units(self):
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
        if self.phase == 5:
            self.next_turn()
        else:
            self.phase += 1
        return

    def get_phase(self):

        return self.phase

    def recruitable(self, n):
        rtr = []
        for pos in self.recruitable_list:
            if pos < n:
                rtr.append(pos)
        return rtr

    def recruit_unit(self, n):
        if n == 0:
            unit = units.Infantry(self.current_player)
        elif n == 1:
            unit = units.Tank(self.current_player)

        if self.current_player not in self.purchases:
            self.purchases[self.current_player] = []

        self.purchases[self.current_player].append(unit)

    def init_turn(self):
        self.deployable_places = self.calculate_purchase_units()
        self.purchase_units = self.calculate_purchase_units()
        self.battles = []

    def conquer_tile(self, tile, new_owner):
        tile.owner = new_owner

    def move_unit(self, from_tile, to_tile, n, unit):
        d = 0
        while True:
            if d == n:
                break
            delta_x = abs(from_tile.cords[0] - to_tile.cords[0])
            delta_y = abs(from_tile.cords[1] - to_tile.cords[1])
            # todo add is legal function instead.
            if delta_x + delta_y <= unit.range:
                if to_tile.owner != self.current_player:
                    if unit.used_steps == 0:
                        unit.set_step(unit.range)
                    else:
                        unit.set_step(delta_x + delta_y)

                    if to_tile.units.__len__() == 0:
                        self.conquer_tile(to_tile, self.current_player)
                    elif not self.battles.__contains__(to_tile.cords):
                        self.battles.append(to_tile.cords)
                else:
                    unit.set_step(delta_y + delta_x)

                unit.set_position(to_tile.cords)
                unit.set_old_position(from_tile.cords)
                if unit.used_steps == unit.range:
                    try:
                        self.movable.remove(unit)
                    except ValueError:
                        print(ValueError.args)

                to_tile.units.append(unit)
                from_tile.units.remove(unit)
                if self.battles.__contains__(from_tile.cords):
                    valid = False
                    for unit in from_tile.units:
                        if unit.owner == self.current_player:
                            valid = True
                            break
                    if not valid:
                        self.battles.remove(from_tile.cords)
                d += 1

    def reset_all_units(self):
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
                # print(unit)
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
        dict_of_nations = dict()
        for nation in self.nations:
            total = 0
            for w in self.map.board:
                for h in w:
                    if h.owner == nation:
                        total += h.units.__len__()
            dict_of_nations[nation] = total

        return dict_of_nations

    def calculate_units(self):
        total = 0
        for w in self.map.board:
            for h in w:
                total += h.units.__len__()
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

    def is_there_a_winner(self):
        winner = True
        for w in self.map.board:
            for h in w:
                if h.owner != self.current_player:
                    winner = False
        return winner

    def find_movable_in_tile(self, cords):
        units = []
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.used_steps < unit.range:
                units.append(unit)
        return units

    def find_unit_count(self, units):
        c = 0
        for key in units:
            for unit in units[key]:
                c += 1
        return c

    def bot(self):
        if not self.current_player.human:
            self.current_player.bot.play_bot(self)