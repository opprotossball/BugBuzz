from abc import ABC, abstractmethod
import numpy as np

class CostModel(ABC):
    @staticmethod
    def evaluate(x, label):
        CostModel.__validate_input(x, label)
        return CostModel.concrete_eval(x,label)

    @abstractmethod
    @staticmethod
    def concrete_eval(x, label):
        pass

    @staticmethod
    def __validate_input(x, label):
        if x is None or label is None:
            raise Exception("Input cannot be None.")
        if not isinstance(x, np.matrix) or not isinstance(label, np.matrix):
            raise Exception("Input has to be instance of numpy.matrix.")
        if label.size != x.size:
            raise Exception("Shape of matrix x and matrix label has to be the same x: " + x.size
                            + " label: " + label.size)

class RMS(CostModel, ABC):
    @staticmethod
    def concrete_eval(x, label):
        mat = x - label
        counter = 0
        sum = 0
        row, col = mat.shape
        for layer in range(row):
            for weight in range(col):
                counter += 1
                sum += mat.item((layer, weight))
        return sum / counter
