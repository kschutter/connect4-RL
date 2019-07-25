import numpy as np
from Board import EMPTY, RED, BLACK, Board
from GameResult import GameResult

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

class RandomishPlayer(Player):
    '''
    Slightly smarter than RandomPlayer - will attempt to play or block winning moves
    '''

    def __init__(self, color):
        super().__init__(color)

    def make_move(self, board):
        '''
        Make winning moves, if none block winning moves, if non random move
        '''

        index = board.random_empty_spot()

        for i in range(board.WIDTH):
            temp_board = Board(state=board.state)
            if temp_board.is_legal(i):
                res, finished = temp_board.move(i, self.color)
                if self.color == res:
                    return board.move(i, self.color)
                elif res == GameResult.RED_WIN or res == GameResult.BLACK_WIN:
                    index = i

        return board.move(index, self.color)
