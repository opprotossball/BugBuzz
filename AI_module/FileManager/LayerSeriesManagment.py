import ast

import numpy as np
import pandas as pd

from AI_module.AI.Layer.Convolutional import Convolutional
from AI_module.AI.Layer.FullyConnected import FullyConnected
from AI_module.AI.Layer.InputLayer import InputLayer
from AI_module.AI.Layer.Layer import valid_layer_short_name

from AI_module.AI.Layer.ActivationModel import valid_am_short_name, get_activation_model


def to_dict(layer):
    mat_w = layer.get_weights()
    mat_b = layer.get_biases()

    if mat_w is not None:
        mat_w = mat_w.tobytes()
    if mat_b is not None:
        mat_b = mat_b.tobytes()
    series = {'l_type': [layer.get_short_name()],
              'l_size': [layer.get_layer_size()],
              'l_prev': [layer.get_previous_size()],
              'l_am': [layer.get_activation_model().get_short_name()],
              'l_w': [mat_w],
              'l_b': [mat_b]}

    return series


def from_series(series):
    __validate(series)

    l_type = series['l_type']

    l_size = int(series['l_size'])
    l_size_prev = int(series['l_prev'])

    l_am = get_activation_model(series['l_am'])

    layer = __get_layer(l_type, l_size, l_am)

    if series['l_w'] is not np.nan:
        decoded_mat = ast.literal_eval(series['l_w'])
        l_weight = np.matrix(np.frombuffer(decoded_mat, dtype=float).reshape((l_size, l_size_prev)))
        layer.set_weights(l_weight)

    if series['l_b'] is not np.nan:
        decoded_mat = ast.literal_eval(series['l_b'])
        l_biases = np.matrix(np.frombuffer(decoded_mat, dtype=float).reshape((1, l_size)))

        layer.set_biases(l_biases)

    return layer


def __get_layer(code, size, am):
    if code == "F":
        return FullyConnected(size, activation_model=am)
    elif code == "I":
        return InputLayer(size, activation_model=am)
    elif code == "C":
        return Convolutional(size, activation_model=am)

def __validate(series):
    if not isinstance(series, pd.Series):
        raise Exception("Given input is not instance of pandas.Series, but was given {}.".format(series.__class__))

    l_type = series['l_type']
    if l_type not in valid_layer_short_name:
        raise Exception("Unknown type of layer: {}".format(series['l_type']))

    l_size = int(series['l_size'])
    if 0 > l_size:
        raise Exception("Invalid size of layer: {}".format(series['l_size']))

    l_size_prev = int(series['l_prev'])
    if 0 > l_size_prev:
        raise Exception("Invalid size of previous layer: {}".format(series['l_prev']))

    l_am = series['l_am']
    if l_am not in valid_am_short_name:
        raise Exception("Unknown type of activation model: {}".format(series['l_am']))

    l_weight = series['l_w']
    if l_weight is None:
        raise Exception("Given weights are None.")

    l_biases = series['l_b']
    if l_biases is None:
        raise Exception("Given biases are None.")
