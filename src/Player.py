import numpy as np
from Board import EMPTY, RED, BLACK

class Player:
    def __init__(self, color=None):
        pass

class RandomPlayer(Player):
    '''
    The dumbest of players - will completely guess each move
    '''

    def __init__(self, color):
        super().__init__(color)

    def make_move(self, board):
        '''
        Only ever make random moves
        '''
        index = board.random_empty_spot()
        return board.move(index, self.color)
