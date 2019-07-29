import tensorflow as tf
import matplotlib.pyplot as plt

import Player
from Board import Board, RED, BLACK
from GameResult import GameResult
from CNNPlayer import CNNPlayer
from NNPlayer import NNQPlayer
from TFSessionManager import TFSessionManager

def play_game(board, player1, player2, dumb, verbose=False):

    board.reset()
    finished = False

    while not finished:

        result, finished = player1.make_move(board, 0)

        if finished:
            if result == GameResult.DRAW:
                final_result = GameResult.DRAW
            else:
                final_result =  GameResult.RED_WIN
        else:
            result, finished = player2.make_move(board, dumb)
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


    p1.final_result(result)
    p2.final_result(result)
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

def play_games(num_games, p1, p2, dumb, verbose=False) -> (int, int, int):
    '''
    Conduct a connect4 game between two given types of players
    num_games times, returning the final scores
    '''
    board = Board()
    p1_wins = p2_wins = draws = 0
    p1.color = RED
    p2.color = BLACK

    for _ in range(num_games):
        result, board = play_game(board, p1, p2, dumb, verbose)
        if result == GameResult.RED_WIN:
            p1_wins += 1
        elif result == GameResult.BLACK_WIN:
            p2_wins += 1
        else:
            draws += 1
        p1.switch_color()
        p2.switch_color()

    return (p1_wins, p2_wins, draws)

def print_stats(red_wins, black_wins, draws):

    red_wins = sum(red_wins)
    black_wins = sum(black_wins)
    draws = sum(draws)
    num_games = red_wins + black_wins + draws
    print(f'''\nAfter {num_games} games we have:\n
            RED wins:\t{red_wins}, {red_wins/num_games*100:.2f}%\n
            BLACK wins:\t{black_wins}, {black_wins/num_games*100:.2f}%\n
            Draws:\t{draws}, {draws/num_games*100:.2f}%\n
            ''')

def eval_players(p1, p2, games_per_set=100, num_sets=100,
                 writer=None, verbose=False):

    '''
    Pit two given players against each other, logging stats over time, not just at the end
    '''

    p1_wins = []
    p2_wins = []
    draws = []
    game_number = []
    game_counter = 0

    for i in range(num_sets):
        p1win, p2win, draw = play_games(games_per_set, p1, p2, i/num_sets, False)
        p1_wins.append(p1win)
        p2_wins.append(p2win)
        draws.append(draw)
        game_counter = game_counter + 1
        game_number.append(game_counter)
        if writer is not None:
            summary = tf.Summary(value=[tf.Summary.Value(tag='Player 1 Win', simple_value=p1win),
                                        tf.Summary.Value(tag='Player 2 Win', simple_value=p2win),
                                        tf.Summary.Value(tag='Draw', simple_value=draw)])
            writer.add_summary(summary, game_counter)

    return game_number, p1_wins, p2_wins, draws

if __name__=='__main__':

    board = Board()
    # CNNPlayer = NNQPlayer(name='CNNPlayer')
    # nnplayer = NNQPlayer(name="NNQPlayer2")
    # cnnplayer = CNNPlayer(name="CNNPlayer")
    randish = Player.RandomishPlayer(RED)
    randish2 = Player.RandomishPlayer(BLACK)
    rand2 = Player.RandomPlayer(RED)

    p1_wins = []
    p2_wins = []
    draws = []
    game_number = []
    game_counter = 0

    num_sets = 10
    games_per_set = 100
    num_training_sets = 100

    TFSessionManager.set_session(tf.Session())

    TFSessionManager.get_session().run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter('log', TFSessionManager.get_session().graph)

    # nnplayer rndplayer mm_player
    p1_t = randish
    p2_t = randish2

    p1 = p1_t
    p2 = p2_t

    # nnplayer.training= False
    # nnplayer2.training= False

    for i in range(num_training_sets):
        p1win, p2win, draw = play_games(games_per_set, p1_t, p2_t, 0, False)
        p1_wins.append(p1win)
        p2_wins.append(p2win)
        draws.append(draw)
        game_counter = game_counter + 1
        game_number.append(game_counter)
        printProgressBar (i, num_training_sets)

    # nnplayer.training= False
    # nnplayer2.training= False

    for i in range(num_sets):
        p1win, p2win, draw = play_games(games_per_set, p1, p2, 0, False)
        p1_wins.append(p1win)
        p2_wins.append(p2win)
        draws.append(draw)
        game_counter = game_counter + 1
        game_number.append(game_counter)
        printProgressBar (i, num_sets)

    writer.close()
    TFSessionManager.set_session(None)

    p = plt.plot(game_number, draws, 'r-', game_number, p1_wins, 'g-', game_number, p2_wins, 'b-')
    plt.title("CNN Player vs One-Ahead Player")

    plt.show()
