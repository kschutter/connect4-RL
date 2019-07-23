import numpy as np
import tensorflow as tf

from GameResult import GameResult
from Board import Board, EMPTY, RED, BLACK, BOARD_SIZE, WIDTH

class QNetwork:

    def add_dense_layer(self, input_tensor, output_size, activation_fn=None,
                        name=None):
        '''
        Adds a dense Neural Net layer to network input_tensor
        '''
        return tf.layers.dense(input_tensor, output_size, activation=activation_fn,
                               kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                               name=name)

    def build_graph(self, name):
        '''
        Builds a new TensorFlow graph with scope 'name'
        '''
        with tf.variable_scope(name, num_nodes=9):
            self.input_positions = tf.placeholder(tf.float32, shape=(None, BOARD_SIZE * 3), name='inputs')

            self.target_input = tf.placeholder(tf.float32, shape=(None, BOARD_SIZE), name='targets')

            net = self.input_positions

            net = self.add_dense_layer(net, BOARD_SIZE * 3 * num_nodes, tf.nn.relu)

            self.q_values = self.add_dense_layer(net, WIDTH, name='q_values')

            self.probabilities = tf.nn.softmax(self.q_values, name='probabilities')
            mse = tf.losses.mean_squared_error(predictions=self.q_values, labels=self.target_input)
            self.train_step = tf.train.GradientDescentOptimizer(learning_rate=self.learningRate)
                                                                .minimize(mse, name='train')
class NNPlayer:

    def __init__(self, color):
        self.color = color

    def state_to_binary(self, color):
        '''
        return self.state as a binary table representation
        '''
        return np.array([(self.state == self.color).astype(int),
                         (self.state == self.color * -1).astype(int),
                         (self.state == EMPTY).astype(int)]).reshape(-1)
