import numpy as np
from .tile import Tile


class MapClass(object):
    def __init__(self, size, nations):
        ###Tuples, with height and width.

        self.size = size

        # A list of Nations, and how many provinces they should have.
        self.nations = nations

        self.board = self.createBoard()

    def createBoard(self):
        board = np.empty(self.size, dtype=Tile)
        number_of_provinces = int((self.size[0]*self.size[1])/self.nations.__len__())


        #Creates the tiles.
        counter = 1
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                board[h][w] = Tile(cords=(h, w))
                if w >= (self.size[1] / (self.nations.__len__()) * counter):
                    counter += 1
                if not board[h][w].water:
                    board[h][w].owner = self.nations[counter-1]
            counter = 1

        #Connects the tiles together and assign start owner.
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                #Edge detection
                if h+1 < self.size[0]:
                    board[h][w].neighbours.append(board[h+1][w])
                if h-1 >= 0:
                    board[h][w].neighbours.append(board[h-1][w])
                if w+1 < self.size[1]:
                    board[h][w].neighbours.append(board[h][w+1])
                if w-1 >= 0:
                    board[h][w].neighbours.append(board[h][w-1])
                '''
                print("h: "+str(h), w)
                for k in board[h][w].neighbours:
                    print(k.cords)
        
        '''
        '''
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                if w >= (self.size[1]/(self.nations.__len__())*counter):
                    counter+=1
                    #print(counter)
                board[h][w].owner = self.nations[counter-1][0]
                #print(board[h][w].owner)
            counter = 1

        '''
        #print(board[3][3].owner)
        '''
        for h in range(self.size[0]):
            for w in range(self.size[1]):
                print(board[h][w].owner, board[h][w].cords)
        '''
        #print(board)
        return board
