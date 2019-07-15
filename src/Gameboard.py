import numpy as np
from IPython.display import HTML, display

class GameBoard:

    RED = 1
    YELLOW = 2

    def __init__(self, width, height):

        self.height = height
        self.board = np.zeros((height, width), dtype=int)

    def make_move(self, index):

        # Transpose the board, to loop through the row not column
        tboard = *self.board

        try:
            for spot in tboard[i::-1]:
                if not spot:
                    spot

    def print_board(self):
        display(HTML("""
        <style>
        .rendered_html table, .rendered_html th, .rendered_html tr, .rendered_html td {
          border: 1px  black solid !important;
          color: black !important;
        }
        </style>
        """+board.html_str()))

board = GameBoard(4,4)
