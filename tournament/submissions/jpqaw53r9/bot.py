from axis_and_allies.bot import Bot
from axis_and_allies.game import Game


class SuperBot(Bot):
    '''
    Read in bot.py for instructions about the different phases.
    '''

    def non_combat_movement_phase(self, game: Game):
        """
        This will force the bot to always advance towards the enemy
        In the non-combat moving phase.
        """
        game.border_tiles = game.calculate_border()
        while len(game.movable) > 0:
            unit = game.movable[0]
            position = unit.get_position()
            new_tile = (-1, None)
            possible_tiles = []
            for tile in game.map.board[position[0]][position[1]].neighbours:
                if tile.owner == unit.owner:
                    for border_tile in game.border_tiles:
                        value = game.calculate_distance_between_tiles(tile, border_tile)
                        if new_tile[0] > value or new_tile[1] is None:
                            new_tile = (value, tile)
                            if value == 0:
                                possible_tiles.append(tile)
            if new_tile[0] == 0:
                min_units = (-1, None)
                for tile in possible_tiles:
                    if len(tile.units) < min_units[0] or min_units[1] is None:
                        min_units = (len(tile.units), tile)
                game.move_unit_friendly(game.map.board[position[0]][position[1]], new_tile[1], unit)
            elif new_tile[0] == -1:
                game.movable.remove(game.movable[0])
            elif new_tile[1] is not None:
                game.move_unit_friendly(game.map.board[position[0]][position[1]], new_tile[1], unit)
        game.next_phase()

    def prioritize_casualties(self, game: Game, values):
        """
        This bot will prioritize to delete infs over tanks.
        """
        to_be_deleted = dict()
        if 'Inf' in values[0]:
            if len(values[0]['Inf']) >= values[1]:
                for unit in values[0]['Inf']:
                    if unit.type not in to_be_deleted:
                        to_be_deleted[unit.type] = []
                    to_be_deleted[unit.type].append(unit)
                    if len(to_be_deleted[unit.type]) == values[1]:
                        break
            elif len(values[0]['Inf']) < values[1]:
                for unit in values[0]['Inf']:
                    if unit.type not in to_be_deleted:
                        to_be_deleted[unit.type] = []
                    to_be_deleted[unit.type].append(unit)
                    diff = values[1] - len(to_be_deleted[unit.type])

                for unit in values[0]['Tank']:
                    if unit.type not in to_be_deleted:
                        to_be_deleted[unit.type] = []
                    to_be_deleted[unit.type].append(unit)
                    if len(to_be_deleted[unit.type]) == diff:
                        break

        elif 'Tank' in values[0]:
            for unit in values[0]['Tank']:
                if unit.type not in to_be_deleted:
                    to_be_deleted[unit.type] = []
                to_be_deleted[unit.type].append(unit)
                if len(to_be_deleted[unit.type]) == values[1]:
                    break

        for key in to_be_deleted:
            game.take_casualties(to_be_deleted, to_be_deleted[key][0].type, len(to_be_deleted[key]))