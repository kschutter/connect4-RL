import numpy as np

class RandomPlayer:
    '''
    The dumbest of players - will completely guess each move
    '''

    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        index = np.random.randint(0, board.WIDTH)
        legal = board.is_legal(index)
        while not legal:
            index = np.random.randint(0, board.WIDTH)
            legal = board.is_legal(index)

        return board.move(self.color, index)
