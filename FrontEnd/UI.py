import pygame
from BackEnd.Robal import *
from random import randrange
from BackEnd.Armia import Armia


class UI:
    def __init__(self, gameMaster):
        self.tileButtons = []
        self.gameMaster = gameMaster

    def setTileButtons(self, tilebutons):
        self.tileButtons = tilebutons

    def selectArmy(self, tile):
        tiles = []
        bug = tile.bug
        if bug is not None and bug.army is not None:
            for anotherBug in bug.army.bugList:
                tiles.append(anotherBug.field)
        return tiles

        # Useless test function
    def drawRandomBug(self, tile):
        x = randrange(8)
        bug = None
        if x == 0:
            bug = Zuk("C")
        elif x == 1:
            bug = Zuk("B")
        elif x == 2:
            bug = Pajak("C")
        elif x == 3:
            bug = Pajak("B")
        elif x == 4:
            bug = Mrowka("C")
        elif x == 5:
            bug = Mrowka("B")
        elif x == 6:
            bug = Konik("C")
        elif x == 7:
            bug = Konik("B")
        bug.setField(tile)
        tile.setBug(bug)
        if bug.side == "B":
            self.gameMaster.WhitePlayer.bugList.append(bug)
        elif bug.side == "C":
            self.gameMaster.BlackPlayer.bugList.append(bug)

    def onTileClick(self):
        for tileButton in self.tileButtons:
            if tileButton.isClickedLeft():
                buttonTile = tileButton.tile
                self.gameMaster.display.highlightedTiles = self.selectArmy(buttonTile)
            if tileButton.isClickedRight():
                buttonTile = tileButton.tile
                self.drawRandomBug(buttonTile)
                self.gameMaster.getArmies("C")
                self.gameMaster.getArmies("B")

