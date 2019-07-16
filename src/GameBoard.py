import numpy as np
from IPython.display import HTML, display

RED = 1
BLACK = -1

class GameBoard:

    def __init__(self, width, height, board=None, connect_num=4):

        # If no previous board given, start with a blank board
        if not board:
            self.board = np.zeros((height, width), dtype=int)
        else:
            self.board = board

        self.connect_num = connect_num - 1

        # Calculate which player moves next, with RED always starting on an empty board
        self.next_player = BLACK if np.sum(self.board) > 0 else RED

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

                self.print_board(x=index, y=idx)
                return True
        except IndexError:
            pass

        print("Invalid move!")
        return False

    def check_win(self, x, y):

        def check_row(row):
            count = 0
            last_color = 1
            for spot in row:
                if spot:
                    if spot == last_color:
                        count += 1
                        if count == self.connect_num:
                            return True
                    else:
                        count = 0
                    last_color = spot
            return False

        vert = check_row(self.board[y])
        np.rot90(self.board, 3)
        horz = check_row(self.board[x])
        np.rot90(self.board, 1)

        print(f"horzwin = {horz}, verwin = {vert}")

        return True if horz or vert else False

    def print_board(self, x, y):
        # display(HTML("""
        # <style>
        # .rendered_html table, .rendered_html th, .rendered_html tr, .rendered_html td {
        #   border: 1px  black solid !important;
        #   color: black !important;
        # }
        # </style>
        # """+board.html_str()))
        print(self.board)
        if self.check_win(x, y):
            print("Winner!\n\n")
        else:
            next = "RED" if self.next_player == RED else "BLACK"
            print(f"Next player: {next}({self.next_player})")

if __name__=='__main__':

    board = GameBoard(width=4, height=4, connect_num=3)

    while(True):
        kb = input("Index of next move, or non-int to quit: ")
        try:
            board.make_move(int(kb))
        except ValueError:
            print("\nEnding Game")
            break
