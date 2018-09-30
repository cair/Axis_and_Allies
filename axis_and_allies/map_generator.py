import numpy as np


class MapClass(object):
    def __init__(self, size, nations):

        self.size = size

        # A list of Nations, and how many provinces they should have.
        self.nations = nations

        self.board = self.create_board()

    def create_board(self):
        board = np.empty(self.size, dtype=Tile)

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


class Tile(object):
    def __init__(self, cords, name='nameless', water=False):
        self.owner = None

        self.neighbours = []

        self.cords = cords

        self.units = []

        self.constructions = []

        self.water = water

        self.value = 2

    def __repr__(self):
        return self.owner.name+self.units.__str__()+self.constructions.__str__()