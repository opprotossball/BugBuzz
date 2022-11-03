from BackEnd.GameObjects.Robal import *
from random import randrange
from FrontEnd.HatchButton import HatchButton
import pygame


class UI:
    def __init__(self, gameMaster):
        self.tileButtons = []
        self.hatchButtons = []
        self.gameMaster = gameMaster
        self.selectedTile = None

        self.antHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/antHatchButton.png")
        self.grasshooperHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperHatchButton.png")
        self.spiderHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/spiderHatchButton.png")
        self.beetleHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/beetleHatchButton.png")
        self.antHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/antHatchButtonSelected.png")
        self.grasshooperHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperHatchButtonSelected.png")
        self.spiderHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/spiderHatchButtonSelected.png")
        self.beetleHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/beetleHatchButtonSelected.png")

        self.hatchButtons.append(HatchButton(self.antHatchButton, self.antHatchButtonSelected, "M"))
        self.hatchButtons.append(HatchButton(self.grasshooperHatchButton, self.grasshooperHatchButtonSelected, "K"))
        self.hatchButtons.append(HatchButton(self.spiderHatchButton, self.spiderHatchButtonSelected, "P"))
        self.hatchButtons.append(HatchButton(self.beetleHatchButton, self.beetleHatchButtonSelected, "Z"))

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
        if tile.bug is not None:
            return
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
        bug.moveBugTo(tile)
        if bug.side == "B":
            self.gameMaster.WhitePlayer.bugList.append(bug)
        elif bug.side == "C":
            self.gameMaster.BlackPlayer.bugList.append(bug)

    def getInput(self):
        for tileButton in self.tileButtons:
            if tileButton.isClickedLeft():
                tile = tileButton.tile
                if tile.bug is None:
                    if not self.makeMove(tile):
                        self.selectedTile = None
                else:
                    self.selectedTile = tile
                selectedArmyTiles = self.selectArmy(tile)
                self.gameMaster.display.highlightedTiles = selectedArmyTiles
            if tileButton.isClickedRight():
                buttonTile = tileButton.tile
                self.drawRandomBug(buttonTile)
                self.gameMaster.getArmies("C")
                self.gameMaster.getArmies("B")

        for hatchButton in self.hatchButtons:
            if hatchButton.isClickedLeft():
                print(hatchButton.bugShortName)

    def makeMove(self, tile):
        if self.selectedTile is None:
            return False
        dictionary = self.selectedTile.getDictionary()
        directions = [d for d, n in dictionary.items() if n == tile]
        if directions.__len__() == 0:
            return False
        direction = directions[0]
        leader = self.selectedTile.bug
        leader.army.performMove(direction)
        self.selectedTile = leader.field
        self.gameMaster.getArmies(leader.side)
        self.gameMaster.display.highlightedTiles = self.selectArmy(tile)
        return True
