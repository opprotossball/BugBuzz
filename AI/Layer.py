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
        self._activation_model = activation_model
        self._layer_size = layer_size

        self._previous_layer = None
        self._activation_state = None

        self._weights = None
        self._biases = None

        self._delta = None

    @abstractmethod
    def __evaluate_concrete(self, input):
        pass

    @abstractmethod
    def __learn_concrete(self, cost, rate):
        pass

    def evaluate(self, input):
        self.__validate_input_is_compilable_with_this_layer_input(input)
        self.__evaluate_concrete(input)

    def learn(self, cost, rate):
        self.__validate_input_is_compilable_with_this_layer_input(cost)
        self.__learn_concrete(cost, rate)

    def set_previous_layer(self, layer):
        self.__previous_layer = layer

    def get_activation_state(self):
        return self._activation_state

    def __validate_input_is_matrix(self, x):
        if x is None:
            raise Exception("Input cannot be None.")
        if not isinstance(x, np.matrix):
            raise Exception("Input has to be instance of numpy.matrix.")

    def __validate_input_is_compilable_with_this_layer_input(self, x):
        self.__validate_input_is_matrix(x)
        if self._layer_size != x.size[0] and self._layer_size != x.size[1]:
            raise Exception("Input has to be compilable with layer of size " + self.__layer_size + ".")


class InputLayer(Layer, ABC):
    def __evaluate_concrete(self, input):
        self.activation_state = input

    def __learn_concrete(self, cost, rate):
        pass


class FullConnected(Layer, ABC):
    def __evaluate_concrete(self, input):
        self.__activation_state = np.dot(input, self._weights) + self._biases
        map(self._activation_model.activation, self._activation_state)

    def __learn_concrete(self, cost, rate):
        out = np.dot(self._weights, self._previous_layer.get_activation_state()) + self._biases
        map(self._activation_model.activation_derivative, out)
        self._delta = np.multiply(cost, out)

        self._previous_layer.learn()    # !VERY IMPORTANT!

        der = np.dot(self._previous_layer.activation_state, self._delta)
        self._weights = self._weights - der * rate
        self._biases = self._biases - self._delta * rate


class Convolutional(Layer, ABC):
    pass
