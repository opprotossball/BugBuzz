class Trader:
    def __init__(self):
        self.GrassHopperPrice = 1
        self.AntPrice = 1
        self.SpiderPrice = 2
        self.BeetlePrice = 3

    def getOptions(self, available):
        options = []
        if (available >= self.GrassHopperPrice):
            options.append(0)
        if available >= self.AntPrice:
            options.append(1)
        if available >= self.SpiderPrice:
            options.append(2)
        if available >= self.BeetlePrice:
            options.append(3)
        options.append(4)  # Pass
        return options

    def buyBug(self, option, available):
        if option in self.getOptions(available):
            price = 0
            if option == 0:
                price = 1
            elif option == 1:
                price = 1
            elif option == 2:
                price = 2
            elif option == 3:
                price = 3
            return option, price
