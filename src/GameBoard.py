import numpy as np

RED = 1
BLACK = -1
ACTIVE = 0
DRAW = 2

class GameBoard:

    def __init__(self, width, height, board=None, connect_num=4):

        # If no previous board given, start with a blank board
        if not board:
            self.board = np.zeros((height, width), dtype=int)
            self.state = ACTIVE
        else:
            check_win()
            self.board = board

        self.connect_num = connect_num - 1
        self.last_move = (0,0)
        self.num_moves = np.sum(np.abs(self.board))

        # Calculate which player moves next, with RED always starting on an empty board
        self.next_player = RED if self.num_moves % 2 == 0 else BLACK

# Make one move at the specified location with the specified color
    def make_move(self, index, player=None):

        # If player unspecified, assume game is played correctly
        if not player:
            player = self.next_player

        # Check if the correct player is attempting a move
        if player is not self.next_player:
            print("Wrong player attempting to make a move")
            return False

        # Rotate self.board so we can iterate through rows and not columns
        nboard = np.rot90(self.board, 3)

        try:
            for idx, spot in enumerate(nboard[::-1][index]):
                if nboard[index][idx]:
                    continue
                nboard[index][idx] = self.next_player
                self.next_player *= -1
                self.board = np.rot90(nboard, 1)
                self.last_move = (index, idx)
                if sum(self.board.shape) == self.num_moves:
                    self.state = DRAW
                return True
        except IndexError:
            pass

        print("Invalid move!")
        return False

    def check_win(self):

        x, y = self.last_move

        def check_row(row):
            print(row)
            count = 0
            last_color = 2
            for spot in row:
                if spot:
                    if spot == last_color:
                        count += 1
                        if count == self.connect_num:
                            self.state = self.next_player * -1
                            return True
                    else:
                        count = 0
                    last_color = spot
            return False

        # Check horizontal win
        horizontal = check_row(self.board[x])

        # Check vertical win
        rotated_board = np.rot90(self.board, 3)
        vertical = check_row(rotated_board[x])

        return vertical or horizontal

    def print_board(self):
        # display(HTML("""
        # <style>
        # .rendered_html table, .rendered_html th, .rendered_html tr, .rendered_html td {
        #   border: 1px  black solid !important;
        #   color: black !important;
        # }
        # </style>
        # """+board.html_str()))
        print(self.board)
        if not self.check_win():
            next = "RED" if self.next_player == RED else "BLACK"
            print(f"Next player: {next}({self.next_player})")

if __name__=='__main__':

    board = GameBoard(width=4, height=4, connect_num=3)

    pre_input = input("Welcome to connect4! Press Enter to Start: ")

    while(True):
        try:
            if pre_input:
                for d in map(int, pre_input):
                    print(f"\nplacing at column {d}")
                    board.make_move(d)
                    board.print_board()
                    if board.check_win():
                        print("Winner!\n")
                        break
                    elif board.state == DRAW:
                        print("Draw!\n")
                        break
                print("\nEnding Game")
                break
            else:
                kb = input("Index of next move(s), or non-int to quit: ")
                move = int(kb)
                board.print_board()
                if board.check_win():
                    print("Winner!\n")
                    break
        except ValueError:
            print("\nEnding Game")
            break

#                           0011223
