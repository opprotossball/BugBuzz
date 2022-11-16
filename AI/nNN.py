import AI.CostModels as cm
from AI.Layer import InputLayer


class nNN:
    def __init__(self):
        self.__layers = []
        self.__input_layer = None
        self.__output_layer = None
        self.__number_of_layers = 0
        self.is_finalized = False

    def evaluate_at(self, x):
        self.__validate_if_finalized()
        self.__input_layer.activation_state = x
        for layer in self.__layers:
            layer.evaluate()
        return self.__output_layer.activation_state

    def learn(self, x, label, rate):
        res = self.evaluate_at(x)
        cost = res - label
        self.__layers[-1].back_propagation(cost, rate)

    def put_layer(self, layer):
        if self.__number_of_layers == 0 and layer.__class__ != InputLayer:
            raise Exception("First layer has to be instance of Layer.InputLayer, not: " + str(layer.__class__) + ".")
        self.__layers.append(layer)
        self.__number_of_layers += 1

    def finalize(self):
        if self.__number_of_layers != 1:
            for layer in range(self.__number_of_layers - 1, 0, -1):
                self.__layers[layer].set_previous_layer(self.__layers[layer - 1])
                self.__layers[layer].generate_if_needed_and_finalize()

        self.__input_layer = self.__layers[0]
        self.__output_layer = self.__layers[-1]
        self.is_finalized = True

    def cost(self, x, label):
        result = self.evaluate_at(x)
        return cm.CostModel.RMS_eval(result, label)

    def __validate_if_finalized(self):
        if not self.is_finalized:
            raise Exception("Can't perform any action on none finalize model.")
