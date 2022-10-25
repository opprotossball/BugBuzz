class Trader:
    def __init__(self):
        self.GrassHopperPrice = 1
        self.AntPrice = 1
        self.SpiderPrice = 2
        self.BeetlePrice = 3

    def getOptions(self, available):
        options = []
        if (available >= self.GrassHopperPrice):
            options.append("GrassHopper")
        if available >= self.AntPrice:
            options.append("Ant")
        if available >= self.SpiderPrice:
            options.append("Spider")
        if available >= self.BeetlePrice:
            options.append("Beetle")
        return options

    def buyBug(self, option, available):
        if option in self.getOptions(available):
            price = 0
            if option == "GrassHopper":
                price = 1
            elif option == "Ant":
                price = 1
            elif option == "Spider":
                price = 2
            elif option == "Beetle":
                price = 3
            return option, price
