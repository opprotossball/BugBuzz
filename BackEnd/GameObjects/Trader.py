from BackEnd.GameObjects.Robal import Konik, Mrowka, Pajak, Zuk


class Trader:
    def __init__(self):
        self.GrassHopperPrice = 1
        self.AntPrice = 1
        self.SpiderPrice = 2
        self.BeetlePrice = 3

    def getOptions(self, player):
        options = []
        if player.resources >= self.GrassHopperPrice:
            options.append("Konik")
        if player.resources >= self.AntPrice:
            options.append("Mrowka")
        if player.resources >= self.SpiderPrice:
            options.append("Pajak")
        if player.resources >= self.BeetlePrice:
            options.append("Zuk")
        return options

    def buyBug(self,  player, option):
        if option in self.getOptions(player):
            robal = 0
            if option == "Konik":
                robal = Konik(player.side)
                player.resources -= 1
            elif option == "Mrowka":
                robal = Mrowka(player.side)
                player.resources -= 1
            elif option == "Pajak":
                robal = Pajak(player.side)
                player.resources -= 2
            elif option == "Zuk":
                robal = Zuk(player.side)
                player.resources -= 3

            player.bugList.append(robal)

            return robal
        return None
