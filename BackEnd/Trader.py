from BackEnd.Robal import Konik, Mrowka, Pajak, Zuk


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

    def buyBug(self, option, available, side):
        if option in self.getOptions(available):
            robal = 0
            price = 0
            if option == "GrassHopper":
                robal = Konik(side)
                price = 1
            elif option == "Ant":
                robal = Mrowka(side)
                price = 1
            elif option == "Spider":
                robal = Pajak(side)
                price = 2
            elif option == "Beetle":
                robal = Zuk(side)
                price = 3
            return robal, price
