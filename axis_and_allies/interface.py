from axis_and_allies.game import Game, GameManager
from axis_and_allies.units import Infantry, Tank


class Interface:

    def purchase_inf(self, game: Game):
        game.recruit_unit(0)


    def purchase_tank(self, game: Game):
        game.recruit_unit(1)


    def next_phase(self, game):
        game.next_phase()


    def select_inf(self, game):
        for unit in game.movable:
            if game.phase == 2 or game.phase == 3:
                if type(unit) == Infantry:
                    return True, unit
            else:
                return False, None


    def select_tank(self, game):
        for unit in game.movable:
            if game.phase == 2 or game.phase == 3:
                if type(unit) == Tank:
                    return True, unit
            else:
                return False, None


    def move_right(self, game, unit):
        if unit is None:
            return False

        tile = game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[1] < len(tile.cords[1])-1:
            new_tile = game.map.board[tile.cords[0]][tile.cords[1]+1]
            game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False


    def move_left(self, game, unit):
        if unit is None:
            return False
        tile = game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[1] > 0:
            new_tile = game.map.board[tile.cords[0]][tile.cords[1]-1]
            game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False


    def move_up(self, game, unit):
        if unit is None:
            return False
        tile = game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[0] > 0:
            new_tile = game.map.board[tile.cords[0]-1][tile.cords[1]]
            game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False


    def move_down(self, game, unit):
        if unit is None:
            return False
        tile = game.map.board[unit.position[0]][unit.position[1]]
        if tile.cords[0] < len(tile.cords[0]):
            new_tile = game.map.board[tile.cords[0]+1][tile.cords[1]]
            game.move_unit(tile, new_tile, 1, unit)
            return True
        else:
            return False
