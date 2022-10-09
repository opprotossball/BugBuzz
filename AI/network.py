import random

import pandas as pd
import numpy as np

import math


class InputNode:
    def __init__(self, value):
        self.value = value


class Neuron:
    def __init__(self, random_init=False, strength_of_the_relation=[], bias=0, threshold=0.5, amplifier_parameter=1,
                 value=0, number_of_pre_neurons=20):
        self.number_of_pre_neuron = number_of_pre_neurons
        self.value = value
        self.strength_of_the_relation = strength_of_the_relation
        self.bias = bias
        self.g = amplifier_parameter
        self.threshold = threshold

        if random_init:
            self.number_of_pre_neuron = number_of_pre_neurons
            self.value = 0
            self.strength_of_the_relation = np.random.randome(number_of_pre_neurons)
            self.g = amplifier_parameter
            self.threshold = random.random()

    def evaluate_my_self(self, pre_neuron_activation_value):  # McCulloch-Pitts Model of the neuron
        h = 0
        for i in range(self.number_of_pre_neuron):
            h += self.strength_of_the_relation[i] * pre_neuron_activation_value[i]
        self.value = f(h - self.threshold, self.g)

    def getStats(self):
        stats = []
        for relation in self.strength_of_the_relation:
            stats.append(relation)
        stats.append(self.threshold)
        stats.append(self.bias)
        return stats


def f(x, g):
    return 1 / (1 + math.exp(-g * x))


def addNoise(value, noise):
    if value + noise > 1:
        return 1
    elif value + noise < -1:
        return -1
    else:
        return value + noise


class NeuralNetwork:
    def __init__(self, input=63, hidden_layers=2, hidden_neurons=(20, 20), output_data=1, init_data_frame=None):
        self.input = [InputNode(0) for i in range(input)]
        self.hidden_layers = []
        if init_data_frame is None:
            if len(hidden_neurons) >= 1:
                self.hidden_layers = [
                    [Neuron(random_init=True, number_of_pre_neurons=input) for i in range(hidden_neurons(0))]]
            for i in range(hidden_layers):
                self.hidden_layers.append([])
                for j in range(1, hidden_neurons[i]):
                    self.hidden_layers[i].append(Neuron(random_init=True, number_of_pre_neurons=hidden_neurons[i - 1]))
            self.output_data = [0 for i in range(output_data)]

            self.dataFrame = pd.DataFrame()

            for layer in range(len(self.hidden_layers)):
                for neuron in range(len(self.hidden_layers[layer])):
                    self.dataFrame[str(layer) + "," + str(neuron)] = np.array(
                        self.hidden_layers[layer][neuron].getStats())
        else:
            last_layer_ID = -1
            for columnName, columnData in init_data_frame:
                layerID, nodeID = columnData.split(separtor=',')
                if layerID != last_layer_ID:
                    last_layer_ID = layerID
                    self.hidden_layers.append([])
                relation = columnData[0:-2]
                threshold = columnData[-1]
                bias = columnData[-2]
                neuron = Neuron(strength_of_the_relation=relation, bias=bias, threshold=threshold, number_of_pre_neurons=len(relation))
                self.hidden_layers[last_layer_ID].append(neuron)

    def getDataFrame(self):
        df = pd.DataFrame()
        for layer in len(self.hidden_layers):
            for neuron in len(self.hidden_layers[layer]):
                self.dataFrame[str(layer) + "," + str(neuron)] = np.array(self.hidden_layers[layer][neuron].getStats())
        return df

    def breed(self, other_data_frame, number_of_offspring, noise=0.01):
        offspring = []
        for i in range(number_of_offspring):
            df = pd.DataFrame()
            for columnName, data in self.dataFrame:
                for gen in range(len(data)):
                    parent = random.randint(0, 2)
                    concrete_noise = noise * (random.random() * 2 - 1)
                    if parent == 0:  # breeding rule
                        df[columnName][gen] = addNoise(self.dataFrame[columnName][gen], concrete_noise)
                    else:
                        df[columnName][gen] = addNoise(other_data_frame[columnName][gen], concrete_noise)
            offspring.append(NeuralNetwork(df))
