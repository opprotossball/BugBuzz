from BackEnd.GameObjects.Robal import *
from random import randrange
from FrontEnd.HatchButton import HatchButton
import pygame


class UI:
    def __init__(self, game_master):
        self.tileButtons = []
        self.hatchButtons = []
        self.game_master = game_master
        self.selected_tile = None
        self.chosenToHatch = None
        self.mode = None
        self.side = None

        self.antHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/antWhiteHatchButton.png")
        self.grasshooperHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperWhiteHatchButton.png")
        self.spiderHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/spiderWhiteHatchButton.png")
        self.beetleHatchButton = pygame.image.load("./FrontEnd/Assets/Buttons/beetleWhiteHatchButton.png")

        self.antHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/antWhiteSelectedHatchButton.png")
        self.grasshooperHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/grasshooperWhiteSelectedHatchButton.png")
        self.spiderHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/spiderWhiteSelectedHatchButton.png")
        self.beetleHatchButtonSelected = pygame.image.load("./FrontEnd/Assets/Buttons/beetleWhiteSelectedHatchButton.png")

        self.hatchButtons.append(HatchButton(self.antHatchButton, self.antHatchButtonSelected, "M"))
        self.hatchButtons.append(HatchButton(self.grasshooperHatchButton, self.grasshooperHatchButtonSelected, "K"))
        self.hatchButtons.append(HatchButton(self.spiderHatchButton, self.spiderHatchButtonSelected, "P"))
        self.hatchButtons.append(HatchButton(self.beetleHatchButton, self.beetleHatchButtonSelected, "Z"))

        self.phase_titles = [
            "White's combat phase",
            "White's move phase",
            "White's hatch phase",
            "Black's combat phase",
            "Black's move phase",
            "Black's hatch phase"
        ]

        self.tip_texts = [
            "Select opponent's army to attack"
            "Select and move your army"
            "Hatch bug in your hatchery"
            "Wait for opponent to play"
            "Wait for opponent to play"
            "Wait for opponent to play"
        ]

    def setMode(self, mode, side):
        self.mode = mode
        self.side = side

    def setTileButtons(self, tilebutons):
        self.tileButtons = tilebutons

    def selectArmy(self, tile):
        tiles = []
        bug = tile.bug
        if bug is not None and bug.army is not None:
            for anotherBug in bug.army.bugList:
                tiles.append(anotherBug.field)
        return tiles

    def getInput(self):
        if self.mode == "Move":
            for tileButton in self.tileButtons:
                if tileButton.isClickedLeft():
                    tile = tileButton.tile
                    if tile.bug is None:
                        if not self.makeMove(tile):
                            self.selected_tile = None
                    else:
                        self.selected_tile = tile
                    selected_army_tiles = self.selectArmy(tile)
                    self.game_master.display.highlightedTiles = selected_army_tiles

        for hatchButton in self.hatchButtons:
            if hatchButton.isClickedLeft():
                self.chosenToHatch = hatchButton.bugShortName

    def makeMove(self, tile):
        if self.selected_tile is None:
            return False
        dictionary = self.selected_tile.getDictionary()
        directions = [d for d, n in dictionary.items() if n == tile]
        if directions.__len__() == 0:
            return False
        direction = directions[0]
        leader = self.selected_tile.bug
        leader.army.performMove(direction)
        self.selected_tile = leader.field
        self.game_master.getArmies(leader.side)
        self.game_master.display.highlightedTiles = self.selectArmy(tile)
        return True
