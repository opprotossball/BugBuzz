import AI.CostModels as cm


class nNN():
    def __init__(self, cost_model=cm.RMS):
        self.__cost_model = cost_model

        self.__layers = []
        self.__number_of_layers = 0
        self.is_finalized = False

    def evaluate(self, x):
        evaluated = x
        for layer in self.__layers:
            evaluated = layer.evaluate(evaluated)
        return evaluated

    def learn(self, x, label, rate):
        cost = x - label
        for layer in range(self.__number_of_layers - 1):
            cost = self.__layers[layer].learn(cost, rate)


    def finalize(self):
        pass

    def cost(self, x, label):
        result = self.evaluate(x)
        return self.__cost_model.evaluate(x, label)
