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
    row, col = matrix.shape
    for layer in range(row):
        for weight in range(col):
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
    MAX_EVAL = 10

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

    def generate_random(self, neuron_distribution_in_layers):
        for i in range(self.number_of_layers + 1):
            if i == 0:
                input_layer = np.random.rand(neuron_distribution_in_layers[i], 1)
            else:
                weights = np.matrix(
                    -1 + 2 * np.random.rand(neuron_distribution_in_layers[i - 1], neuron_distribution_in_layers[i]))
                biases = np.matrix(-1 + 2 * np.random.rand(1, neuron_distribution_in_layers[i]))
                self.weights_of_the_layers.append(weights.T)
                self.biases_of_the_layer.append(biases.T)

    def learn(self, input, label, rate):
        last_index = self.number_of_layers
        last_weight_index = self.number_of_layers - 1
        size_of_output = self.neuron_distribution_in_layers[last_index]

        if not isinstance(label, np.matrix):
            raise Exception("Label has to be instace of numpy.matrix")

        if label.shape != (1, size_of_output,):
            label = label.T

        W = self.weights_of_the_layers.copy()
        B = self.biases_of_the_layer.copy()
                                                                                    # <Getting inputs>
        X = input.T
        outputs = [X]

        for layer in range(self.number_of_layers):
            X = np.dot(W[layer], X)
            #X += B[layer] // TODO
            map(activation_f, X)

            mat = np.matrix(X.copy())
            outputs.append(mat)
                                                                                    # </Getting inputs>
                                                                                    # <Getting deltas>
        deltas = [[] for layer in range(last_index)]

        outputs[last_index] = np.matrix(outputs[last_index])
        cost = outputs[last_index] - label.T

        derivative = np.dot(W[last_weight_index], outputs[last_index - 1])
        map(derivative_f, derivative)

        deltas[last_weight_index] = np.multiply(cost, derivative)

        for layer in range(last_weight_index - 1, -1, -1):
            cost = np.dot(deltas[layer + 1].T, W[layer + 1])
            derivative = np.dot(W[layer], outputs[layer])
            map(derivative_f, derivative)
            deltas[layer] = np.multiply(derivative, cost.T)
                                                                                    # </Getting deltas>
                                                                                    # <Getting new weights>
        newW = [[] for layer in self.weights_of_the_layers]

        for layer in range(1, last_index + 1):
            derivative = np.dot(outputs[layer].T, deltas[layer - 1])
            newW[layer - 1] = W[layer - 1] - derivative.T * rate
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

    def cost_function(self, input, labels):
        eval = self.evaluate_at(np.matrix(input))
        label = np.matrix(labels)
        cost = 0
        costMat = eval - label
        map(lambda x: x**2, costMat)
        row, col = costMat.shape
        for layer in range(row):
            for value in range(col):
                cost += costMat.item((layer, value))
        return cost / len(input)

    def evaluate_at(self, X):
        if X.shape != (1, self.neuron_distribution_in_layers[0]):
            raise Exception("Wrong size input! Received: " + X.shape + " Expected: " + str((1, self.neuron_distribution_in_layers[0])) + ".")

        X = X.T
        for i in range(self.number_of_layers):
            X = np.dot(self.weights_of_the_layers[i], X)
            #X += self.biases_of_the_layer[i]
            map(activation_f, X)

        return X.T

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
for i in range(2000):
    mat = nn.learn(np.matrix([1,2,3]), np.matrix([0.5, 1]), 0.5)
    nn.weights_of_the_layers = mat
    print(str(nn.cost_function([1, 2, 3], [0.5, 1])))
