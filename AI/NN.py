import math
import random

import numpy as np
import pandas as pd
from pandas import Series


def activation_f(x):
    return 1 / (1 + math.exp(-x))


def map(func, matrix):
    for layer in matrix:
        for i in range(len(layer)):
            layer[i] = func(layer[i])


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

    def clone(self):
        new = NeuralNetwork()
        for weights in self.weights_of_the_layers:
            mat = weights.copy()
            self.weights_of_the_layers.append(mat)

        for biases in self.biases_of_the_layer:
            mat = biases.copy()
            self.biases_of_the_layer.append(mat)
        return new

    def mutate(self, rate, power):
        for matrix in self.weights_of_the_layers:
            if random.random() < rate:
                map(lambda val: alter_and_standardize(power, val), matrix)

        for matrix in self.biases_of_the_layer:
            if random.random() < rate:
                map(lambda val: alter(power, val), matrix)

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
            X = X.tolist()
            X = np.matrix([[activation_f(cell) for cell in row] for row in X])

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
