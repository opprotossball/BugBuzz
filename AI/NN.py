import math
import random

import numpy as np
import pandas as pd
from pandas import Series


def activation_f(x):
    return 1 / (1 + math.exp(-x))

def derivative_f(x):
    return (math.exp(-x))/(math.exp(-x) + 1)**2

def map(func, matrix):
    for layer in range(len(matrix)):
        for weight in range(len(matrix[layer])):
            newValue = func(matrix.item((layer, weight)))
            matrix.itemset((layer, weight), newValue)


def alter_and_standardize(power, val):
    altered = random.gauss(val, power)
    if altered > 1:
        altered = 1
    elif altered < -1:
        altered = -1
    return altered


def alter(power, val):
    altered = random.gauss(val, power)
    return altered


class NeuralNetwork:
    def __init__(self, neuron_distribution_in_layers=(1, 1), data_frame=None, weights_of_the_layers=None,
                 biases_of_the_layer=None):
        self.weights_of_the_layers = []
        self.biases_of_the_layer = []
        self.number_of_layers = len(neuron_distribution_in_layers) - 1
        self.size_of_input = neuron_distribution_in_layers[0]
        self.neuron_distribution_in_layers = neuron_distribution_in_layers

        self.score = 0

        if weights_of_the_layers is not None and biases_of_the_layer is not None:
            self.weights_of_the_layers = weights_of_the_layers
            self.biases_of_the_layer = biases_of_the_layer
            self.get_distribution()
        elif data_frame is not None:
            self.generate_random(self.neuron_distribution_in_layers)  # TODO change to reading from data frame
        else:
            self.generate_random(self.neuron_distribution_in_layers)

    def learn(self, input, label, rate):
        outputs = [input]
        last_index = len(self.neuron_distribution_in_layers) -1
        size_of_output = self.neuron_distribution_in_layers[last_index]

        if not isinstance(label, np.matrix):
            raise Exception("Label has to be instace of numpy.matrix")
        if label.shape != (1, size_of_output):
            raise Exception("Label has to be size of the output. Expected shape: (1, " + str(size_of_output) +"), provided:" + str(label.shape) + "")

        last_layer_index = len(self.neuron_distribution_in_layers) - 1

        W = self.weights_of_the_layers.copy()

        cost_for_layer = []
                                                                                    # <Getting inputs>
        X = input
        for layer in range(self.number_of_layers):
            cost_for_layer.append([])
            X = np.dot(X, self.weights_of_the_layers[layer])
            X += self.biases_of_the_layer[layer]
            map(activation_f, X)
            mat = np.matrix(X.copy())
            outputs.append(mat)
                                                                                    # </Getting inputs>
        for lab, inp in zip(label, outputs[last_layer_index]):
            cost_for_layer[last_layer_index].append(lab - inp)


        # Ostatnia warstwa: n = nmax
        #    deltan = (xn - ln) [multiply] f'(Wn*x(n-1))

        # Pozostałe warstwy: n < nmax
        #    deltan = W(n+1)T [dot] delta[n+1] [multiply] f'(Wn*x(n-1))

                                                                                    # <Getting deltas>
        deltas = [[] for layer in self.weights_of_the_layers]

        derivative = np.dot(W[last_index], outputs[last_index - 1])
        map(derivative_f, derivative)
        deltas[last_index] = np.multiply((outputs[last_index] - label), derivative)

        for layer in range(len(self.neuron_distribution_in_layers) - 2 , -1, -1):
            cost = np.dot(W[layer + 1].T, deltas[layer + 1])
            derivative = np.dot(W[last_index], outputs[layer - 1])
            map(derivative_f, derivative)
            deltas[layer] = np.multiply(cost, derivative)
                                                                                    # </Getting deltas>
        # Kalkulacja końcowa:
        #    dE/dW = deltan [dot] x(n-1)T
        #    a = rate_of_learning
        #    Wn' = Wn - dE/dW * a
                                                                                    # <Getting new weights>
        newW = [[] for layer in self.weights_of_the_layers]
        for layer in range(len(self.neuron_distribution_in_layers)):
            derivative = np.dot(deltas[layer], outputs[layer].T)
            newW[layer] = W[layer] - derivative * rate
                                                                                    # </Getting new weights>
        return newW

    def cost(self, input, labels):
        eval = self.evaluate_at(input)
        cost = []
        for outcome, label in zip(eval, labels):
            cost.append((outcome - label) ** 2)
        cost = np.matrix(cost)
        return cost

    def clone(self):
        new = NeuralNetwork()
        for weights in self.weights_of_the_layers:
            mat = weights.copy()
            self.weights_of_the_layers.append(mat)

        for biases in self.biases_of_the_layer:
            mat = biases.copy()
            self.biases_of_the_layer.append(mat)
        return new

    def generate_random(self, neuron_distribution_in_layers):
        for i in range(self.number_of_layers + 1):
            if i == 0:
                input_layer = np.random.rand(neuron_distribution_in_layers[i], 1)
            else:
                weights = np.matrix(
                    -1 + 2 * np.random.rand(neuron_distribution_in_layers[i - 1], neuron_distribution_in_layers[i]))
                biases = np.matrix(-1 + 2 * np.random.rand(1, neuron_distribution_in_layers[i]))
                self.weights_of_the_layers.append(weights)
                self.biases_of_the_layer.append(biases)

    def evaluate_at(self, X):
        row, col = X.shape
        if col != self.size_of_input or col != 1:
            print("Wrong size input!")

        for i in range(self.number_of_layers):
            X = np.dot(X, self.weights_of_the_layers[i])
            X += self.biases_of_the_layer[i]
            map(activation_f, X)

        return X

    def get_distribution(self):
        distribution = []
        for layer in self.weights_of_the_layers:
            counter = 0
            for neuron in layer:
                counter += 1
            distribution.append(counter)
        self.neuron_distribution_in_layers = distribution

    def toDataFrame(self, weights_in, biases_in):
        df = pd.DataFrame()

        number_of_layers = len(biases_in)

        for layer in range(number_of_layers):
            weights = weights_in[layer].transpose()
            weights_l = weights.tolist()

            biases_l = biases_in[layer].tolist()[0]

            for neuron in range(len(weights_l)):
                w = Series(weights_l[neuron])
                b = Series(biases_l[neuron])
                s = pd.concat([w, b], ignore_index=True)

                column_name = str(layer) + " " + str(neuron)

                df[column_name] = s
        return df

nn = NeuralNetwork((3,4,2))

nn.learn(np.matrix([1,2,3]), np.matrix([3,4]), 0.1)