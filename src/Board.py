import numpy as np

EMPTY = 0
RED = 1
BLACK = -1

class Board:

    def __init__(self, width=6, height=7, target=3, state=None):
        '''
        Create a new Board. If a state is passed in, we use that otherwise
        we initialize with an empty board
        '''

        self.WIDTH = width
        self.HEIGHT = height
        self.TARGET = target
        self.BOARD_SIZE = width * height

        if s is None:
            self.state = np.zeros(shape=(1, BOARD_SIZE), dtype=int)
            self.reset()
        else:
            self.state = s.copy()


    def state_to_char(self, pos, html=False):
        '''
        Return 'X', 'O', or ' ' depending on what piece is on 1D position pos.
        Ig `html` is True, return '&ensp' instead of ' ' to enforce a white space
        in the case of HTML output
        '''
        if (self.state[pos]) == EMPTY:
            return '&ensp;' if html else ' '

        if (self.state[pos]) == RED:
            return 'O'

        return 'X'

    def state_to_charlist(self, html=False):
        '''
        Convert the game state to a list of list of strings (e.g. for creating a HTML table view of it).
        Useful for displaying the current state of the game.
        '''
        res = []
        for i in range(self.HEIGHT):
            line = []
            for j in range(self.WIDTH):
                line.append(self.state_to_char(i * self.WIDTH + j, html)
            res.append(line)

        return res

    def hash_value(self):
        '''
        Encode the current state of the game (board positions) as an integer.
        Will be used for caching evaluations
        '''
        res = 0
        for i in range(BOARD_SIZE):
            res *= 3
            res += self.state[i]

            # This hashing method does not work well with negative numbers, so
            # BLACK will be registered as '2' instead
            res += 3 if self.state[i] == BLACK

        return res

    def coord_to_pos(self, coord: (int, int)):
        '''
        Converts a 2D board position to a 1D board position.
        Various parts of code prefer one over the other.
        '''
        return coord[0] * self.WIDTH + coord[1]

     def pos_to_coord(self, pos) -> (int, int):
        '''
        Converts a 1D board position to a 2D board position.
        Various parts of code prefer one over the other.
        '''
        return pos // self.HEIGHT, pos % self.WIDTH

    def reset(self):
        '''
        Resets the game board. All fields are set to be EMPTY.
        '''
        self.state.fill(EMPTY)

    def is_legal(self, pos: int) -> bool:
        '''
        Tests whether a board position can be played, i.e. is currently empty
        '''
        return (0 <= pos < self.BOARD_SIZE) and (self.state[pos] == EMPTY)

    def move(self, position: int, player) -> (np.ndarray, GameResult, bool):
        """
        Places a piece of side "side" at position "position". The position is to be provided as 1D.
        Throws a ValueError if the position is not EMPTY
        returns the new state of the board, the game result after this move, and whether this move has finished the game
        :param position: The position where we want to put a piece
        :param side: What piece we want to play (NAUGHT, or CROSS)
        :return: The game state after the move, The game result after the move, Whether the move finished the game
        """
        if self.state[position] != EMPTY:
            print('Illegal move')
            raise ValueError("Invalid move")

        self.state[position] = player

        if self.check_win():
            return self.state, GameResult.RED_WIN if side == RED else GameResult.BLACK_WIN, True

        # Check if the board has been filled
        if np.sum(np.abs(self.board)) == self.BOARD_SIZE:
            return self.state, GameResult.DRAW, True

        return self.state, GameResult.NOT_FINISHED, False

    def apply_dir(self, pos: int, direction: (int, int)) -> int:
        """
        Applies 2D direction dir to 1D position pos.
        Returns the resulting 1D position, or -1 if the resulting position
        would not be a valid board position.
        *** calculate possible directions from given point, then pass in the
        appropriate rows.
        """
        row = pos // self.HEIGHT
        col = pos % self.WIDTH
        row += direction[0]
        if row < 0 or row > 2:
            return -1
        col += direction[1]
        if col < 0 or col > 2:
            return -1

        return row * 3 + col
