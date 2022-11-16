from abc import ABC, abstractmethod

import AI.ActivationModel as am
import numpy as np


def map(func, matrix):
    row, col = matrix.shape
    for layer in range(row):
        for weight in range(col):
            newValue = func(matrix.item((layer, weight)))
            matrix.itemset((layer, weight), newValue)


class Layer(ABC):
    def __init__(self, layer_size, activation_model=am.ReLu):
        self.activation_state = None

        self._activation_model = activation_model
        self._layer_size = layer_size
        self._finalized = False

        self._previous_layer = None

        self._weights = None
        self._biases = None

        self._delta = None

    @abstractmethod
    def _evaluate_concrete(self):
        pass

    @abstractmethod
    def _learn_concrete(self, cost, rate):
        pass

    def evaluate(self):
        self._evaluate_concrete()

    def learn(self, cost, rate):
        self._validate_input_is_compilable_with_this_layer_input(cost)
        self._learn_concrete(cost, rate)

    def set_previous_layer(self, layer):
        self._previous_layer = layer

    def __validate_matrix_massege(self, x, matrix_name="Given matrix"):
        if x is None:
            raise Exception("Input cannot be None.")
        if not isinstance(x, np.matrix):
            raise Exception(str(matrix_name) + " has to be instance of numpy.matrix.")

    def _validate_input_is_compilable_with_this_layer_input(self, x):
        self.__validate_matrix_massege(x, "Input")
        if 1 != x.shape[0] and self._layer_size != x.shape[1]:
            raise Exception("Input has to be compilable with layer of shape. Given:  " + x.shape +
                            " Expected: " + str((1, self._layer_size)) + ".")

    def set_weights(self, weights):
        self.__validate_matrix_massege(weights, "Weights")
        row, col = weights.shape

        if row == col: #TODO
            print("lalla")

        if not self._finalized:
            self._weights = weights
        else:
            raise Exception("Changing weights for finalised layer is forbidden.")

    def set_biases(self, biases):
        self.__validate_matrix_massege(biases, "Biases")
        bias_shape = biases.shape
        expected_shape = (1, self._layer_size)

        if bias_shape != expected_shape:
            raise Exception("Invalid size of bias. Given: " + str(bias_shape) + " Expected: " + str(expected_shape))

        if not self._finalized:
            self._biases = biases
        else:
            raise Exception("Changing biases for finalised layer is forbidden.")

    def get_layer_size(self):
        return self._layer_size

    def generate_if_needed_and_finalize(self):
        if self._biases is None:
            self._biases = np.random.random(self._layer_size) * 2 - 1

        if self._weights is None:
            self._biases = np.random.rand(self._layer_size, self._previous_layer.get_layer_size()) * 2 - 1


class FullConnected(Layer, ABC):
    def _evaluate_concrete(self):
        self._validate_input_is_compilable_with_this_layer_input(self._previous_layer.activation_state)
        self.activation_state = np.dot(self._previous_layer.activation_state, self._weights) + self._biases
        map(self._activation_model.activation, self.activation_state)

    def _learn_concrete(self, cost, rate):
        out = np.dot(self._weights, self._previous_layer.get_activation_state()) + self._biases
        map(self._activation_model.activation_derivative, out)
        self._delta = np.multiply(cost, out)

        self._previous_layer.learn()    # !VERY IMPORTANT!

        der = np.dot(self._previous_layer.activation_state, self._delta)
        self._weights = self._weights - der * rate
        self._biases = self._biases - self._delta * rate


class InputLayer(Layer, ABC):
    def _evaluate_concrete(self):
        pass

    def _learn_concrete(self, cost, rate):
        pass

    def set_biases(self, biases):
        pass

    def set_weights(self, weights):
        pass

    def set_previous_layer_and_finalize(self, layer):
        pass

    def generate_if_needed_and_finalize(self):
        pass

class Convolutional(Layer, ABC):
    pass
