import numpy as np
from .tile import Tile


class MapClass(object):
    def __init__(self, size, nations):

        self.size = size

        # A list of Nations, and how many provinces they should have.
        self.nations = nations

        self.board = self.create_board()

    def create_board(self):
        board = np.empty(self.size, dtype=Tile)
        number_of_provinces = int((self.size[0] * self.size[1]) / self.nations.__len__())

        # Creates the tiles.
        counter = 1
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                board[h][w] = Tile(cords=(h, w))
                if w >= (self.size[1] / (self.nations.__len__()) * counter):
                    counter += 1
                if not board[h][w].water:
                    board[h][w].owner = self.nations[counter - 1]
            counter = 1

        # Connects the tiles together and assign start owner.
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                # Edge detection
                if h + 1 < self.size[0]:
                    board[h][w].neighbours.append(board[h + 1][w])
                if h - 1 >= 0:
                    board[h][w].neighbours.append(board[h - 1][w])
                if w + 1 < self.size[1]:
                    board[h][w].neighbours.append(board[h][w + 1])
                if w - 1 >= 0:
                    board[h][w].neighbours.append(board[h][w - 1])

        return board
