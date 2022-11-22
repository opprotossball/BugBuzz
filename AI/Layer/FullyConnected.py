from abc import ABC
from AI.Layer.Layer import Layer
import numpy as np


class FullyConnected(Layer, ABC):
    _short_name = "F"

    def _evaluate_concrete(self):
        self.activation_state = np.dot(self._previous_layer.activation_state, self._weights) + self._biases
        map(self._activation_model.activation, self.activation_state)

    def _learn_concrete(self, cost, rate):
        out = np.dot(self._previous_layer.activation_state, self._weights)
        map(self._activation_model.activation_derivative, out)
        delta = np.multiply(cost, out)

        n_cost = np.dot(delta, self._weights.T)
        self._previous_layer.back_propagation(n_cost, rate)  # !VERY IMPORTANT!

        derivative = np.dot(self._previous_layer.activation_state.T, delta)
        self._weights -= derivative * rate
        self._biases -= delta * rate

