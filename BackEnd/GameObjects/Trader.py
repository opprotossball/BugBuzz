from BackEnd.GameObjects.Robal import Konik, Mrowka, Pajak, Zuk, RobalEnum


class Trader:
    def __init__(self):
        self.GrassHopperPrice = 1
        self.AntPrice = 1
        self.SpiderPrice = 2
        self.BeetlePrice = 3

    def getOptions(self, available, bugs_available):
        options = []
        if available >= self.GrassHopperPrice and bugs_available[RobalEnum.K] > 0:
            options.append(RobalEnum.K)
        if available >= self.AntPrice and bugs_available[RobalEnum.M] > 0:
            options.append(RobalEnum.M)
        if available >= self.SpiderPrice and bugs_available[RobalEnum.P] > 0:
            options.append(RobalEnum.P)
        if available >= self.BeetlePrice and bugs_available[RobalEnum.Z] > 0:
            options.append(RobalEnum.Z)
        return options

    def buyBug(self, option, player):
        side = player.side
        bug = None
        price = 0
        if option in self.getOptions(player.resources, player.bugs_available):
            if option == RobalEnum.K:
                bug = Konik(side)
                price = 1
            elif option == RobalEnum.M:
                bug = Mrowka(side)
                price = 1
            elif option == RobalEnum.P:
                bug = Pajak(side)
                price = 2
            elif option == RobalEnum.Z:
                bug = Zuk(side)
                price = 3
        return bug, price
