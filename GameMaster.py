from Plansza import Plansza
from InterfejsGracza import InterfejsGracza

from threading import Thread

import time


class GameMaster:
    def __init__(self):
        self.plansza = Plansza(5)
        self.turn = 0

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
            hatchery = self.plansza.blacksHatchery
        elif side == "C":
            hatchery = self.plansza.whitesHatchery
        for hatch in hatchery:
            if not hatch.hasBug():
                return True
        return False


    def GetAvialabelSpaceForHatch(self, side):
        if side == "B":
            hatchery = self.plansza.blacksHatchery
        elif side == "C":
            hatchery = self.plansza.whitesHatchery
            option = []
        for field in hatchery:
            if not field.hasBug():
                option.append(field)
        return option

    def addBug(self, selectedPlacmentField, bugID):
        bug = Robal(bugID)
        selectedPlacmentField.addBug(bug)




GM = GameMaster()

GM.newGame()