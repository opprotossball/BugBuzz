import math
from abc import ABC, abstractmethod

valid_am_short_name = ["SoftMax", "ReLu", "Neutral"]


def get_activation_model(code):
    if code == "SoftMax":
        return SoftMax
    elif code == "ReLu":
        return ReLu
    elif code == "Neutral":
        return Neutral


class ActivationModel(ABC):
    @staticmethod
    @abstractmethod
    def activation(x):
        pass

    @staticmethod
    @abstractmethod
    def activation_derivative(x):
        pass

    @staticmethod
    @abstractmethod
    def get_short_name():
        pass


class SoftMax(ActivationModel, ABC):
    @staticmethod
    def activation(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def activation_derivative(x):
        return (math.exp(-x)) / (math.exp(-x) + 1) ** 2

    @staticmethod
    def get_short_name():
        return "SoftMax"


class ReLu(ActivationModel, ABC):
    @staticmethod
    def activation(x):
        return max(0, x)

    @staticmethod
    def activation_derivative(x):
        if x > 0:
            return 1
        return 0

    @staticmethod
    def get_short_name():
        return "ReLu"


class Neutral(ActivationModel, ABC):
    @staticmethod
    def activation(x):
        return x

    @staticmethod
    def activation_derivative(x):
        return 1

    @staticmethod
    def get_short_name():
        return "Neutral"
