import numpy as np
from GameResult import GameResult

EMPTY = 0
RED = 1
BLACK = -1
BOARD_SIZE = 42

class Board:

    def __init__(self, width=7, height=6, target=4, state=None):
        '''
        Create a new Board. If a state is passed in, we use that otherwise
        we initialize with an empty board
        '''

        self.WIDTH = width
        self.HEIGHT = height
        self.TARGET = target
        self.BOARD_SIZE = width * height

        if state is None:
            self.state = np.zeros(shape=self.BOARD_SIZE, dtype=int)
        else:
            self.state = state.copy()

    def coord_to_pos(self, coord: (int, int)):
        '''
        Converts a 2D board coordinate to a 1D board position.
        Various parts of code prefer one over the other.
        '''
        return coord[0] * self.WIDTH + coord[1]

    def pos_to_coord(self, pos) -> (int, int):
        '''
        Converts a 1D board position to a 2D board coordinate.
        Various parts of code prefer one over the other.
        '''
        return pos // self.WIDTH, pos % self.WIDTH

    def ind_to_pos(self, ind):
        '''
        Converts a column index into the lowest available move, returning
        a 1D position
        '''
        for i in range(self.HEIGHT-1):
            if self.state[ind + self.WIDTH] == EMPTY:
                ind += self.WIDTH
        return ind

    def reset(self):
        '''
        Resets the game board. All fields are set to be EMPTY.
        '''
        self.state.fill(EMPTY)

    def is_legal(self, move):
        '''
        Tests whether a board position can be played, i.e. is currently empty
        '''
        col = move % self.WIDTH
        return self.state[col] == EMPTY and 0 <= col < self.WIDTH

    def move(self, move, player):
        """
        Drops a piece of side "side" at column matching move. The move is to be provided as 1D.
        Throws a ValueError if the position is not EMPTY
        returns the game result after this move, and whether this move has finished the game
        """
        index = move % self.WIDTH
        if not self.is_legal(move):
            print('Illegal move')
            raise ValueError("Invalid move")

        position = self.ind_to_pos(index)

        self.state[position] = player

        if self.check_win(position):
            return (GameResult.RED_WIN if player == RED else GameResult.BLACK_WIN, True)

        # Check if the board has been filled
        if np.sum(np.abs(self.state)) == self.BOARD_SIZE:
            return (GameResult.DRAW, True)

        return (GameResult.NOT_FINISHED, False)

    def random_empty_spot(self):
        '''
        Returns a valid random move index, for exploration
        '''
        index = np.random.randint(0, self.WIDTH)
        while not self.is_legal(index):
            index = np.random.randint(0, self.WIDTH)
        return index

    def check_win_in_row(self, row) -> bool:
        """
        Checks and returns whether there are self.TARGET(int) pieces of the same
        type in a row
        Used internally to check whether either side has won the game.
        """
        if len(row) < self.TARGET:
            return False

        for i in range(len(row) - self.TARGET + 1):
            row_sum = abs(sum(row[i:self.TARGET + i]))
            if row_sum >= self.TARGET:
                return True

        return False

    def check_win(self, pos) -> int:
        '''
        Checks whether either side has won the game
        Returns 0 if no win, and which player won if not
        '''
        row, col = self.pos_to_coord(pos)

        # CHeck horizontal win
        horz_row = self.state[row*self.WIDTH:row*self.WIDTH + self.WIDTH]
        horz_win = self.check_win_in_row(horz_row)

        # Check vertical win
        vert_win = self.check_win_in_row(self.state[col::self.WIDTH])

        # Check diagonal wins
        brow, bcol, frow, fcol = self.get_edges(row, col)
        backd_win = False
        board = self.state.reshape((self.HEIGHT, -1))
        back_diag = board.diagonal(offset=brow-bcol)
        backd_win = self.check_win_in_row(back_diag)

        fowd_win = False
        flip_board = np.fliplr(board)
        for i in range((self.WIDTH-1) * -1, self.HEIGHT):
            for_diag = flip_board.diagonal(offset=i)
            if len(for_diag) >= self.TARGET:
                fowd_win = fowd_win or self.check_win_in_row(for_diag)

        if horz_win or vert_win or backd_win or fowd_win:
            return self.state[pos]
        return 0

    def get_edges(self, row, col):
        '''
        Return the upper-most 2D coordinates corresponding to the forward and backwards
        diagonals based on the given coord
        '''

        brow = row
        bcol = col
        while brow != 0 and bcol != 0:
            brow -= 1
            bcol -= 1

        frow = row
        fcol = col
        while frow != 0 and fcol != self.WIDTH-1:
            frow -= 1
            fcol += 1

        return (brow, bcol, frow, fcol)

    def state_to_char(self, pos, html=False):
        '''
        Return 'X', 'O', or ' ' depending on what piece is on 1D position pos.
        Ig `html` is True, return '&ensp' instead of ' ' to enforce a white space
        in the case of HTML output
        '''
        if (self.state[pos]) == EMPTY:
            return '&ensp;' if html else ' '

        if (self.state[pos]) == RED:
            return 'X'

        return 'O'

    def state_to_charlist(self, html=False):
        '''
        Convert the game state to a list of list of strings (e.g. for creating a HTML table view of it).
        Useful for displaying the current state of the game.
        '''
        res = []
        for i in range(self.HEIGHT):
            line = []
            for j in range(self.WIDTH):
                line.append(self.state_to_char(i * self.WIDTH + j, html))
            res.append(line)

        return res

    def __str__(self):
        """
        Return ASCII representation of the board
        """
        board_str = ""
        for i in range(self.HEIGHT):
            board_str += '|'
            for j in range(self.WIDTH):
                board_str += self.state_to_char(i * self.WIDTH + j)
                if j == self.WIDTH - 1:
                    board_str += '|'
            board_str += "\n"
        return board_str
