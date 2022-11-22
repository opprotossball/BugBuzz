from abc import ABC
from AI.Layer.Layer import Layer


class Convolutional(Layer, ABC):
    _short_name = "C"

    def _evaluate_concrete(self):
        pass

    def _learn_concrete(self, cost, rate):
        pass
