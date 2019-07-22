import numpy as np

class RandomPlayer:

    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        index = np.random.randint(0, board.WIDTH)
        while not board.is_legal(index):
            index = np.random.randint(0, board.WIDTH)
        return (index, self.color)
