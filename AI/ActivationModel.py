import math
from abc import ABC, abstractmethod


class ActivationModel(ABC):
    @abstractmethod
    @staticmethod
    def activation(x):
        pass

    @abstractmethod
    @staticmethod
    def activation_derivative(x):
        pass


class SoftMax(ActivationModel):
    @staticmethod
    def activation(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def activation_derivative(x):
        return (math.exp(-x))/(math.exp(-x) + 1)**2


class ReLu(ActivationModel):
    @staticmethod
    def activation(x):
        return max(0, x)

    @staticmethod
    def activation_derivative(x):
        if x > 0:
            return 1
        return 0
