import numpy as np

class RandomPlayer:

    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        index = np.random.randint(0, board.WIDTH)
        legal = board.is_legal(index)
        while not legal:
            index = np.random.randint(0, board.WIDTH)
            legal = board.is_legal(index)
        return (index, self.color)
