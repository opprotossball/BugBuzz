import pygame
import math
from BackEnd.Plansza import Plansza
from BackEnd.Robal import *
from BackEnd.Armia import Armia
from FrontEnd.TileButton import TileButton
from random import randrange
from pygame.locals import *
from FrontEnd.UI import UI


class Display:

    def __init__(self, gameMaster, windowScreenRatio = 4 / 5, bugRadiusRatio = 1.2, marginRadiusRatio = 1/8, caption='Robale', backgroundColor = (80, 80, 80), tileColor = (153, 153, 153), resourcesColor = (0, 160, 0), hatcheryColor = (150, 45, 45), highlightedColor = (81, 210, 252)):
        pygame.init()

        self.backgroundColor = backgroundColor
        self.tileColor = tileColor
        self.resourcesColor = resourcesColor
        self.hatcheryColor = hatcheryColor
        self.highlightedColor = highlightedColor

        self.width = int(pygame.display.Info().current_w * windowScreenRatio)
        self.height = int(pygame.display.Info().current_h * windowScreenRatio)
        self.xCenter = int(self.width / 2)
        self.yCenter = int(self.height / 2)

        self.gameMaster = gameMaster
        self.tiltAngle = math.pi / 2
        self.screen = None
        self.bugRadiusRatio = bugRadiusRatio
        self.marginRadiusRatio = marginRadiusRatio
        self.bugScale = None
        self.margin = None
        self.tileRadius = None
        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.cos60 = math.cos(math.pi / 3)
        self.sin60 = math.sin(math.pi / 3)
        self.tileButtons = []
        self.highlightedTiles = []

        self.beetleWhite = pygame.transform.flip(pygame.image.load("../FrontEnd/Assets/Bugs/BeetleWhite.png"), True, False)
        self.beetleBlack = pygame.image.load("../FrontEnd/Assets/Bugs/BeetleBlack.png")
        self.spiderWhite = pygame.transform.flip(pygame.image.load("../FrontEnd/Assets/Bugs/SpiderWhite.png"), True, False)
        self.spiderBlack = pygame.image.load("../FrontEnd/Assets/Bugs/SpiderBlack.png")
        self.antWhite = pygame.transform.flip(pygame.image.load("../FrontEnd/Assets/Bugs/AntWhite.png"), True, False)
        self.antBlack = pygame.image.load("../FrontEnd/Assets/Bugs/AntBlack.png")
        self.grasshooperWhite = pygame.transform.flip(pygame.image.load("../FrontEnd/Assets/Bugs/GrasshooperWhite.png"), True, False)
        self.grasshooperBlack = pygame.image.load("../FrontEnd/Assets/Bugs/GrasshooperBlack.png")

        self.resize(self.width, self.height)
        self.screen.fill(self.backgroundColor)
        pygame.display.set_caption(caption)
        self.resize(self.width, self.height)

    def updateWindow(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
        self.gameMaster.UI.onTileClick()
        self.drawTiles()
        self.highlight()
        self.drawBugs()
        pygame.display.update()

    def resize(self, newWidth, newHeight):
        self.screen = pygame.display.set_mode((newWidth, newHeight), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.fill(self.backgroundColor)
        self.width = newWidth
        self.height = newHeight
        self.xCenter = int(newWidth / 2)
        self.yCenter = int(newHeight / 2)
        newRadius = int((0.7 * newWidth / (2 * self.gameMaster.board.size + 1)) / (2 * self.cos30))
        newMargin = int(newRadius * self.marginRadiusRatio)
        if (newRadius * 2 * (self.gameMaster.board.size * 2 + 1) - self.gameMaster.board.size * (2 * (newRadius + newMargin) * self.cos30 * self.cos60)) > newHeight:
            newRadius = int((newHeight / (4 * self.gameMaster.board.size + 1)) / (2 * self.sin30))
            newMargin = int(newRadius * self.marginRadiusRatio)
        self.tileRadius = newRadius
        self.margin = newMargin
        self.bugScale = (self.bugRadiusRatio * newRadius / self.antWhite.get_width())

    def drawHex(self, xCenter, yCenter, radius, color):
        vertices = []
        for i in range(6):
            x = xCenter + radius * math.cos(self.tiltAngle + math.pi * 2 * i / 6)
            y = yCenter + radius * math.sin(self.tiltAngle + math.pi * 2 * i / 6)
            vertices.append([int(x), int(y)])
        return pygame.draw.polygon(self.screen, color, vertices)

    def transformToRealCoordinates(self, pole):
        x = int(self.xCenter + (self.tileRadius + self.margin) * self.cos30 * (pole.s - pole.q))
        y = int(self.yCenter + (self.tileRadius + self.margin) * (self.sin30 * (pole.q + pole.s) - pole.r))
        return (x, y)

    def drawTiles(self):
        tileButtons = []
        for pole in self.gameMaster.board.iterList:
            coordinates = self.transformToRealCoordinates(pole)
            if pole.hatchery:
                color = self.hatcheryColor
            elif pole.resources:
                color = self.resourcesColor
            else:
                color = self.tileColor
            tileButton = TileButton(pole, self.drawHex(coordinates[0], coordinates[1], self.tileRadius, color))
            tileButtons.append(tileButton)
        self.gameMaster.UI.setTileButtons(tileButtons)

    def drawBugs(self):
        for bug in self.gameMaster.BlackPlayer.bugList:
            self.drawBug(bug, bug.field)
        for bug in self.gameMaster.WhitePlayer.bugList:
            self.drawBug(bug, bug.field)

    def drawBug(self, bug, tile):
        coordinates = self.transformToRealCoordinates(tile)
        image = None
        if bug.short_name == "K":
            if bug.side == 'B':
                image = self.grasshooperWhite
            elif bug.side == 'C':
                image = self.grasshooperBlack
        elif bug.short_name == "M":
            if bug.side == 'B':
                image = self.antWhite
            elif bug.side == 'C':
                image = self.antBlack
        elif bug.short_name == "P":
            if bug.side == 'B':
                image = self.spiderWhite
            elif bug.side == 'C':
                image = self.spiderBlack
        elif bug.short_name == "Z":
            if bug.side == 'B':
                image = self.beetleWhite
            elif bug.side == 'C':
                image = self.beetleBlack
        if image is None:
            print("there is no image for ", type(bug), "bug, or bug doesn't have valid side assigned")
            return
        image = pygame.transform.smoothscale(image, (int(image.get_width() * self.bugScale), int(image.get_height() * self.bugScale)))
        self.screen.blit(image, (int(coordinates[0] - image.get_width() / 2), int(coordinates[1] - image.get_height() / 2)))

    def highlight(self):
        for tile in self.highlightedTiles:
            coordinates = self.transformToRealCoordinates(tile)
            self.drawHex(coordinates[0], coordinates[1], self.tileRadius, self.highlightedColor)
