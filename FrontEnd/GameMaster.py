from BackEnd.Armia import Armia
from BackEnd.Plansza import Plansza
from BackEnd.Robal import Robal
from InterfejsGracza import InterfejsGracza

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

    def getArmies(self, side):
        armies = []

        fields_of_plane = self.plansza.iterList

        for pole in fields_of_plane:
            if pole.bug is not None and pole.bug.side == side:
                army = Armia()
                army.addRobal(pole.bug)
                for direction in pole.neighbours:
                    if direction is not None and direction.bug.side == side:
                        army.addRobal(direction.bug)
                        fields_of_plane.remove(direction.bug)
                armies.append(army)


    def isAvailableSpaceForHatch(self, side):
        hatchery = []
        if side == "B":
            hatchery = self.plansza.blacksHatchery
        elif side == "C":
            hatchery = self.plansza.whitesHatchery
        for hatch in hatchery:
            if not hatch.hasBug():
                return True
        return False


    def getAvialabelSpaceForHatch(self, side):
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