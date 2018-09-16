import random as r


from new_bot import Bot


class NewBot(Bot):
    '''def phase_1(self, game):
        """
        This bot will only produce inf
        """
        used = 0
        while True:
            pos = game.recruitable(game.purchase_units - used)
            if pos.__len__() == 0:
                game.next_phase()
                break
            game.recruit_unit(0)
            used += pos[0]
    '''
    def calculate_distance_between_tiles(self, tile_1, tile_2):
        x, y = tile_1.cords[0], tile_1.cords[1]
        x2, y2 = tile_2.cords[0], tile_2.cords[1]

        return abs(x-x2)+abs(y-y2)
    '''
    def phase_2(self, game):
        """
        Forces the bot to attack if possible, otherwise towards the border.
        """
        game.battles = []
        while game.movable.__len__() > 0:
            if r.random() > 0.1:
                unit = game.movable[0]
                position = unit.get_position()
                hit = False
                for tile in game.map.board[position[0]][position[1]].neighbours:
                    if tile.owner != game.current_player:
                        self.moved[tile.cords.__str__()] = position
                        game.move_unit(game.map.board[position[0]][position[1]], tile, 1, unit)
                        hit = True
                        break
                if not hit:
                    new_tile = (9999, None)
                    for tile in game.map.board[position[0]][position[1]].neighbours:
                        for border_tile in game.border_tiles:
                            value = self.calculate_distance_between_tiles(tile, border_tile)
                            if new_tile[0] > value:
                                new_tile = (value, tile)
                    if new_tile[1] is not None:
                        game.move_unit(game.map.board[position[0]][position[1]], new_tile[1], 1, unit)
            else:
                break
        game.phase = 2.5
    '''
    def phase_3(self, game):
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
                        value = self.calculate_distance_between_tiles(tile, border_tile)
                        if new_tile[0] > value or new_tile[1] is None:
                            new_tile = (value, tile)
                            if value == 0:
                                possible_tiles.append(tile)
            if new_tile[0] == 0:
                min_units = (-1, None)
                for tile in possible_tiles:
                    if len(tile.units) < min_units[0] or min_units[1] is None:
                        min_units = (len(tile.units), tile)
                game.move_unit(game.map.board[position[0]][position[1]], new_tile[1], 1, unit)
            elif new_tile[0] == -1:
                game.movable.remove(game.movable[0])
            elif new_tile[1] is not None:
                game.move_unit(game.map.board[position[0]][position[1]], new_tile[1], 1, unit)
        game.next_phase()

    def prioritize_casualties(self, game, values):
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



