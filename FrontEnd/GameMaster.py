from BackEnd.Armia import Armia
from BackEnd.Plansza import Plansza
from BackEnd.Robal import Robal
from InterfejsGracza import InterfejsGracza

import time


class GameMaster:
    def __init__(self):
        self.plansza = Plansza(5)
        self.turn = 0

    def newGame(self, player_white, player_black):
        self.BlackPlayer = player_black
        self.WhitePlayer = player_white

        while(True):
            print("Tura białego atak.")
            self.WhitePlayer.performAttack()
            time.sleep(0.5)
            print("Tura białego ruch.")
            self.WhitePlayer.performMove()
            time.sleep(0.5)
            print("Tura białego wylęganie.")
            self.WhitePlayer.performHatchery()
            time.sleep(0.5)
            print("Tura czarnego atak.")
            self.BlackPlayer.performAttack()
            time.sleep(0.5)
            print("Tura czarnego ruch.")
            self.BlackPlayer.performMove()
            time.sleep(0.5)
            print("Tura czarnego wylęganie.")
            self.BlackPlayer.performHatchery()
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
            if hatch.bug is not None:
                return True
        return False


    def getAvialabelSpaceForHatch(self, side):
        if side == "B":
            hatchery = self.plansza.blacksHatchery
        elif side == "C":
            hatchery = self.plansza.whitesHatchery
            option = []
        for hatch in hatchery:
            if hatch.bug is not None:
                option.append(hatch)
        return option

    def addBug(self, selectedPlacmentField, bugID):
        bug = Robal(bugID)
        selectedPlacmentField.addBug(bug)

    def setUI(self, ui):
        self.ui = ui
        ui.drawBoard(self.plansza, ui.width / 2, ui.height / 2, 40, 3)
        ui.updateWindow()

    def updateWindow(self):
        self.ui.updateWindow()