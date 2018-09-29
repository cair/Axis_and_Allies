from axis_and_allies.game import Game, GameManager
from axis_and_allies.units import Infantry, Tank


class BaseBot:
    def __init__(self, game):
        self.game = game
        self.tiles = 

    def next_phase(self):
        self.game.next_phase()

    def select_inf(self):
        for unit in self.game.movable:
            if self.game.phase == 2 or self.game.phase == 3:
                if type(unit) == Infantry:
                    return True, unit
            else:
                return False, None

    def select_tank(self):
        for unit in self.game.movable:
            if self.game.phase == 2 or self.game.phase == 3:
                if type(unit) == Tank:
                    return True, unit
            else:
                return False, None

    def move_right(self, unit):
        tile = self.game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[1] < len(tile.cords[1])-1:
            new_tile = self.game.map.board[tile.cords[0]][tile.cords[1]+1]
            self.game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False

    def move_left(self, unit):
        tile = self.game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[1] > 0:
            new_tile = self.game.map.board[tile.cords[0]][tile.cords[1]-1]
            self.game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False

    def move_up(self, unit):
        tile = self.game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[0] > 0:
            new_tile = self.game.map.board[tile.cords[0]-1][tile.cords[1]]
            self.game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False

    def move_down(self, unit):
        tile = self.game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[0] < len(tile.cords[0]):
            new_tile = self.game.map.board[tile.cords[0]+1][tile.cords[1]]
            self.game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False

from axis_and_allies.nation import Nation
Germany = Nation()
Game = Game((4,4))