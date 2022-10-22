import math
import time

import numpy as np


def activation_f(x):
    return 1 / (1 + math.exp(-x))


class NeuralNetwork:
    def __init__(self, neuron_distribution_in_layers, data_frame=None):
        self.weights_of_the_layers = []
        self.biases_of_the_layer = []
        self.number_of_layers = len(neuron_distribution_in_layers)
        self.size_of_input = neuron_distribution_in_layers[0]
        if data_frame is None:
            for i in range(self.number_of_layers):
                if i == 0:
                    input_layer = np.random.rand(neuron_distribution_in_layers[i], 1)
                else:
                    weights = np.matrix(-1+2*np.random.rand(neuron_distribution_in_layers[i - 1], neuron_distribution_in_layers[i]))
                    biases = np.matrix(-1+2*np.random.rand(1, neuron_distribution_in_layers[i]))
                    self.weights_of_the_layers.append(weights)
                    self.biases_of_the_layer.append(biases)
        else:
            # TODO dataFrame reading
            print("I am working, on it.")

    def evaluate_at(self, X):
        row, col = X.shape
        if col != self.size_of_input:
            print("Wrong size input!")

        for i in range(self.number_of_layers - 1):
            X = np.dot(X, self.weights_of_the_layers[i])
            X += self.biases_of_the_layer[i]
            lX = X.tolist()
            X = np.matrix([[activation_f(cell) for cell in row] for row in lX])

        return X

    def toDataFrame(self):
        # TODO dataFrame writing
        print("I am working, on it")

start = time.time()
n = NeuralNetwork([63, 20, 20, 1])
print(n.evaluate_at(np.matrix([1,2])))
end = time.time()
print("Wykonano w czasie: " + str(end-start))

# np.array([f(xi) for xi in x])
