from abc import ABC
from AI.Layer.Layer import Layer


class InputLayer(Layer, ABC):
    _short_name = "I"

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
