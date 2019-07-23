from Players import RandomPlayer
from Board import Board, RED, BLACK
from GameResult import GameResult

def play_game(board, player1, player2, verbose=False):

    board.reset()
    current_player = RED
    finished = False

    while not finished:

        _, result, finished = player1.make_move(board)

        if finished:
            if result == GameResult.DRAW:
                final_result = GameResult.DRAW
            else:
                final_result =  GameResult.RED_WIN
        else:
            _, result, finished = player2.make_move(board)
            if finished:
                if result == GameResult.DRAW:
                    final_result =  GameResult.DRAW
                else:
                    final_result =  GameResult.BLACK_WIN
        if verbose:
            if result == GameResult.RED_WIN:
                print("RED wins!")
            elif result == GameResult.BLACK_WIN:
                print("BLACK wins!")

    return final_result, board

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def play_games(num_games, red_player, black_player) -> (int, int, int):
    '''
    Conduct a connect4 game between two given types of players
    num_games times, returning the final scores
    '''
    board = Board()
    p1 = red_player(RED)
    p2 = black_player(BLACK)
    p1_wins = p2_wins = draws = 0

    for _ in range(num_games):
        result, board = play_game(board, p1, p2)
        if result == GameResult.RED_WIN:
            p1_wins += 1
        elif result == GameResult.DRAW:
            draws += 1

        printProgressBar (_, num_games)

    return (p1_wins, num_games-p1_wins-draws, draws)

if __name__=='__main__':

    num_games = 10000
    red_wins, black_wins, draws = play_games(num_games, RandomPlayer, RandomPlayer)
    print(f'''\nAfter {num_games} games we have:\n
            RED wins:\t{red_wins}, {red_wins/num_games*100:.2f}%\n
            BLACK wins:\t{black_wins}, {black_wins/num_games*100:.2f}%\n
            Draws:\t{draws}, {draws/num_games*100:.2f}%\n
            ''')
