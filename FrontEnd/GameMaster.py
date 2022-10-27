from BackEnd.Armia import Armia
from BackEnd.Plansza import Plansza


class GameMaster:
    def __init__(self):
        self.plansza = Plansza(5)
        self.turn = 0

        self.BlackPlayer = None
        self.WhitePlayer = None

    def newGame(self, player_white, player_black):
        self.BlackPlayer = player_black
        self.WhitePlayer = player_white
        while True:
            print("Tura białego atak.")
            self.WhitePlayer.resources += self.getResourcesForSide("B")
            self.WhitePlayer.performAttack()
            #time.sleep(0.5)
            print("Tura białego ruch.")
            self.WhitePlayer.performMove()
            #time.sleep(0.5)
            print("Tura białego wylęganie.")
            self.WhitePlayer.performHatchery()
            #time.sleep(0.5)
            print("Tura czarnego atak.")
            self.BlackPlayer.resources += self.getResourcesForSide("C")
            self.BlackPlayer.performAttack()
            #time.sleep(0.5)
            print("Tura czarnego ruch.")
            self.BlackPlayer.performMove()
            #time.sleep(0.5)
            print("Tura czarnego wylęganie.")
            self.BlackPlayer.performHatchery()
            #time.sleep(0.5)

    def getArmies(self, side):
        armies = []

        if side == "B":
            player = self.WhitePlayer
        elif side == "C":
            player = self.BlackPlayer
        else:
            return

        for bug in player.bugList:
            bug.army = None

        for bug in player.bugList:
            if bug.army is not None:
                break
            army = Armia()
            army.addBug(bug)
            bug.recruitNeighbours()
            army.setMoves()
            armies.append(army)

        return armies

    def getResourcesForSide(self, side):
        resources = self.plansza.resources
        self.getArmies(side)
        n = 1
        for field in resources:
            if field.bug is not None and field.bug.side == side:
                n += field.bug.army.numberOfGrassHopppers
        return n

    def isAvailableSpaceForHatch(self, side):
        hatchery = []
        if side == "B":
            hatchery = self.plansza.whitesHatchery
        elif side == "C":
            hatchery = self.plansza.blacksHatchery

        for hatch in hatchery:
            if hatch.bug is None:
                return True
        return False

    def getAvialabelSpaceForHatch(self, side):
        if side == "B":
            hatchery = self.plansza.whitesHatchery
        elif side == "C":
            hatchery = self.plansza.blacksHatchery
        option = []
        for hatch in hatchery:
            if hatch.bug is not None:
                option.append(hatch)
        return option

    def setUI(self, ui):
        self.ui = ui
        ui.drawBoard(self.plansza, ui.width / 2, ui.height / 2, 40, 3)
        ui.updateWindow()

    def updateWindow(self):
        self.ui.updateWindow()