from BackEnd.Plansza import Plansza
from BackEnd.Robal import Robal
from InterfejsGracza import InterfejsGracza
from FrontEnd.UI import UI
from FrontEnd.Display import Display

import time


class GameMaster:
    def __init__(self):
        self.board = Plansza(4)
        self.turn = 0
        self.UI = UI(self)
        self.display = Display(self)
        self.display.run()

    def newGame(self):
        self.BlackPlayer = InterfejsGracza("C", self)
        self.WhitePlayer = InterfejsGracza("B", self)
        while(True):
            print("Tura białego atak.")
            self.WhitePlayer.Attack()
            time.sleep(0.5)
            print("Tura białego ruch.")
            self.WhitePlayer.Move()
            time.sleep(0.5)
            print("Tura białego wylęganie.")
            self.WhitePlayer.Hatch()
            time.sleep(0.5)
            print("Tura czarnego atak.")
            self.BlackPlayer.Attack()
            time.sleep(0.5)
            print("Tura czarnego ruch.")
            self.BlackPlayer.Move()
            time.sleep(0.5)
            print("Tura czarnego wylęganie.")
            self.BlackPlayer.Hatch()
            time.sleep(0.5)

    def isAvialabelSpaceForHatch(self, side):
        hatchery = []
        if side == "B":
            hatchery = self.board.blacksHatchery
        elif side == "C":
            hatchery = self.board.whitesHatchery
        for hatch in hatchery:
            if not hatch.hasBug():
                return True
        return False

    def getAvialabelSpaceForHatch(self, side):
        if side == "B":
            hatchery = self.board.blacksHatchery
        elif side == "C":
            hatchery = self.board.whitesHatchery
            option = []
        for field in hatchery:
            if not field.hasBug():
                option.append(field)
        return option

    def addBug(self, selectedPlacmentField, bugID):
        bug = Robal(bugID)
        selectedPlacmentField.addBug(bug)


if __name__ == '__main__':
    gm = GameMaster()
