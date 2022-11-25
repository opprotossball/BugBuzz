from BackEnd.GameObjects.Robal import Konik, Mrowka, Pajak, Zuk


class Trader:
    def __init__(self):
        self.GrassHopperPrice = 1
        self.AntPrice = 1
        self.SpiderPrice = 2
        self.BeetlePrice = 3

    def getOptions(self, available, bugs_available):
        options = []
        if available >= self.GrassHopperPrice and bugs_available['K'] > 0:
            options.append('K')
        if available >= self.AntPrice and bugs_available['M'] > 0:
            options.append('M')
        if available >= self.SpiderPrice and bugs_available['P'] > 0:
            options.append('P')
        if available >= self.BeetlePrice and bugs_available['Z'] > 0:
            options.append('Z')
        return options

    def buyBug(self, option, player):
        side = player.side
        bug = None
        price = 0
        if option in self.getOptions(player.resources, player.bugs_available):
            if option == 'K':
                bug = Konik(side)
                price = 1
            elif option == 'M':
                bug = Mrowka(side)
                price = 1
            elif option == 'P':
                bug = Pajak(side)
                price = 2
            elif option == 'Z':
                bug = Zuk(side)
                price = 3
        return bug, price
