from Players import RandomPlayer
from Board import Board
from GameResult import GameResult

RED = 1
BLACK = -1

def play_game(board, player1, player2):

    board.reset()
    current_player = RED
    finished = False

    while not finished:

        move, color = player1.make_move(board)
        print(board.is_legal(move))
        _, result, finished = board.move(move, color)
        print(board)

        if finished:
            if result == GameResult.DRAW:
                final_result = GameResult.DRAW
            else:
                final_result =  GameResult.RED_WIN
        else:
            move, color = player2.make_move(board)
            _, result, finished = board.move(move, color)
            print(board)
            if finished:
                if result == GameResult.DRAW:
                    final_result =  GameResult.DRAW
                else:
                    final_result =  GameResult.BLACK_WIN

        if result == GameResult.RED_WIN:
            print("RED wins!")
        elif result == GameResult.BLACK_WIN:
            print("BLACK wins!")

    return final_result

if __name__=='__main__':
    board = Board()
    player1 = RandomPlayer(RED)
    player2 = RandomPlayer(BLACK)

    print(play_game(board, player1, player2))
