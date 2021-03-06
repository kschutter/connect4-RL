import numpy as np
import tensorflow as tf
from TFSessionManager import TFSessionManager as TFSN

from Board import Board, BOARD_SIZE, EMPTY, RED, BLACK
from Player import Player
from GameResult import GameResult


class QNetwork:
    '''
    Contains a TensorFlow graph which is suitable for learning the Tic Tac Toe Q function
    '''

    def __init__(self, name, learning_rate):
        """
        Constructor for QNetwork. Takes a name and a learning rate for the GradientDescentOptimizer
        """
        self.learningRate = learning_rate
        self.name = name
        self.input_positions = None
        self.target_input = None
        self.q_values = None
        self.probabilities = None
        self.train_step = None
        self.build_graph(name)

    def add_dense_layer(self, input_tensor: tf.Tensor, output_size, activation_fn=None,
                        name=None):
        """
        Adds a dense Neural Net layer to network input_tensor
        """
        return tf.layers.dense(input_tensor, output_size, activation=activation_fn,
                               kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                               name=name)

    def build_graph(self, name):
        '''
        Builds a new TensorFlow graph with scope `name`
        name: The scope for the graph. Needs to be unique for the session.
        '''
        with tf.variable_scope(name):
            self.input_positions = tf.placeholder(tf.float32, shape=(None, BOARD_SIZE * 3), name='inputs')

            self.target_input = tf.placeholder(tf.float32, shape=(None, BOARD_SIZE), name='targets')

            net = self.input_positions

            net = self.add_dense_layer(net, BOARD_SIZE * 3 * 9, tf.nn.relu)

            self.q_values = self.add_dense_layer(net, BOARD_SIZE, name='q_values')

            self.probabilities = tf.nn.softmax(self.q_values, name='probabilities')
            mse = tf.losses.mean_squared_error(predictions=self.q_values, labels=self.target_input)
            self.train_step = tf.train.GradientDescentOptimizer(learning_rate=self.learningRate).minimize(mse,
                                                                                                          name='train')


class NNQPlayer(Player):
    '''
    Implements a Tic Tac Toe player based on a Reinforcement Neural Network learning the Tic Tac Toe Q function
    '''

    def switch_color(self):
        super()

    def board_state_to_nn_input(self, state):
        """
        Converts a Tic Tac Tow board state to an input feature vector for the Neural Network. The input feature vector
        is a bit array of size 27. The first 9 bits are set to 1 on positions containing the player's pieces, the second
        9 bits are set to 1 on positions with our opponents pieces, and the final 9 bits are set on empty positions on
        the board.
        """
        res = np.array([(state == self.color).astype(int),
                        (state == (self.color * -1)).astype(int),
                        (state == EMPTY).astype(int)])
        return res.reshape(-1)

    def __init__(self, name, reward_discount=0.95, win_value=1.0, draw_value=0.0,
                 loss_value=-1.0, learning_rate=0.01, training=True):
        '''
        Constructor for the Neural Network player.
        '''
        tf.reset_default_graph()
        self.reward_discount = reward_discount
        self.win_value = win_value
        self.draw_value = draw_value
        self.loss_value = loss_value
        self.color = None
        self.board_position_log = []
        self.action_log = []
        self.next_max_log = []
        self.values_log = []
        self.name = name
        self.nn = QNetwork(name, learning_rate)
        self.training = training
        super().__init__()

    def new_game(self, color):
        '''
        Prepares for a new games. Store which side we play and clear internal data structures for the last game.
        '''
        self.color = color
        self.board_position_log = []
        self.action_log = []
        self.next_max_log = []
        self.values_log = []

    def calculate_targets(self):
        '''
        Based on the recorded moves, compute updated estimates of the Q values for the network to learn
        '''
        game_length = len(self.action_log)
        targets = []

        for i in range(game_length):
            target = np.copy(self.values_log[i])

            target[self.action_log[i]] = self.reward_discount * self.next_max_log[i]
            targets.append(target)

        return targets

    def get_probs(self, input_pos):
        '''
        Feeds the feature vector `input_pos` which encodes a board state into the Neural Network and computes the
        Q values and corresponding probabilities for all moves (including illegal ones).
        '''
        probs, qvalues = TFSN.get_session().run([self.nn.probabilities, self.nn.q_values],
                                                feed_dict={self.nn.input_positions: [input_pos]})
        return probs[0], qvalues[0]

    def make_move(self, board):
        '''
        Implements the Player interface and makes a move on Board `board`
        '''

        # We record all game positions to feed them into the NN for training with the corresponding updated Q
        # values.
        self.board_position_log.append(board.state.copy())

        nn_input = self.board_state_to_nn_input(board.state)
        probs, qvalues = self.get_probs(nn_input)
        qvalues = np.copy(qvalues)

        # We filter out all illegal moves by setting the probability to -1. We don't change the q values
        # as we don't want the NN to waste any effort of learning different Q values for moves that are illegal
        # anyway.
        for index, p in enumerate(qvalues):
            if not board.is_legal(index):
                probs[index] = -1

        # Our next move is the one with the highest probability after removing all illegal ones.
        move = np.argmax(probs)  # int

        # Unless this is the very first move, the Q values of the selected move is also the max Q value of
        # the move that got the game from the previous state to this one.
        if len(self.action_log) > 0:
            self.next_max_log.append(qvalues[move])

        # We record the action we selected as well as the Q values of the current state for later use when
        # adjusting NN weights.
        self.action_log.append(move)
        self.values_log.append(qvalues)

        # We execute the move and return the result
        res, finished = board.move(move, self.color)
        return res, finished

    def final_result(self, result):
        '''
        This method is called once the game is over. If `self.training` is True, we execute a training run for
        the Neural Network.
        '''

        # Compute the final reward based on the game outcome
        if (result == GameResult.RED_WIN and self.color == RED) or (
                result == GameResult.BLACK_WIN and self.color == BLACK):
            reward = self.win_value  # type: float
        elif (result == GameResult.BLACK_WIN and self.color == RED) or (
                result == GameResult.RED_WIN and self.color == BLACK):
            reward = self.loss_value  # type: float
        elif result == GameResult.DRAW:
            reward = self.draw_value  # type: float
        else:
            raise ValueError("Unexpected game result {}".format(result))

        # The final reward is also the Q value we want to learn for the action that led to it.
        self.next_max_log.append(reward)

        # If we are in training mode we run the optimizer.
        if self.training:
            # We calculate our new estimate of what the true Q values are and feed that into the network as
            # learning target
            targets = self.calculate_targets()

            # We convert the input states we have recorded to feature vectors to feed into the training.
            nn_input = [self.board_state_to_nn_input(x) for x in self.board_position_log]

            # We run the training step with the recorded inputs and new Q value targets.
            TFSN.get_session().run([self.nn.train_step],
                                   feed_dict={self.nn.input_positions: nn_input, self.nn.target_input: targets})
