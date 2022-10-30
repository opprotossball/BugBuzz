import pygame
import math

from FrontEnd.GameMaster import GameMaster
from FrontEnd.InterfejsGracza import InterfejsGracza
from BackEnd.Plansza import Plansza
from BackEnd.Robal import *
from random import randrange
from pygame.locals import *


class TileButton:
    clicked = False

    def __init__(self, pole, polygon):
        self.tile = pole
        self.polygon = polygon

    def isClicked(self):
        mousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 0:
            TileButton.clicked = False
        elif self.polygon.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1 and not TileButton.clicked:
            TileButton.clicked = True
            return True
        else:
            return False


class UI:

    def __init__(self, startBoard, windowScreenRatio = 4 / 5, bugRadiusRatio = 1.2, marginRadiusRatio = 1/8, caption='Robale', backgroundColor = (80, 80, 80), tileColor = (153, 153, 153), resourcesColor = (0, 160, 0), hatcheryColor = (150, 45, 45)):
        pygame.init()

        self.backgroundColor = backgroundColor
        self.tileColor = tileColor
        self.resourcesColor = resourcesColor
        self.hatcheryColor = hatcheryColor

        self.width = int(pygame.display.Info().current_w * windowScreenRatio)
        self.height = int(pygame.display.Info().current_h * windowScreenRatio)
        self.xCenter = int(self.width / 2)
        self.yCenter = int(self.height / 2)

        self.tiltAngle = math.pi / 2
        self.board = startBoard
        self.screen = None
        self.bugRadiusRatio = bugRadiusRatio
        self.marginRadiusRatio = marginRadiusRatio
        self.bugScale = None
        self.margin = None
        self.running = True
        self.tileRadius = None
        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.cos60 = math.cos(math.pi / 3)
        self.sin60 = math.sin(math.pi / 3)
        self.tileButtons = []

        self.beetleWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/BeetleWhite.png"), True, False)
        self.beetleBlack = pygame.image.load("Assets/Bugs/BeetleBlack.png")
        self.spiderWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/SpiderWhite.png"), True, False)
        self.spiderBlack = pygame.image.load("Assets/Bugs/SpiderBlack.png")
        self.antWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/AntWhite.png"), True, False)
        self.antBlack = pygame.image.load("Assets/Bugs/AntBlack.png")
        self.grasshooperWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/GrasshooperWhite.png"), True, False)
        self.grasshooperBlack = pygame.image.load("Assets/Bugs/GrasshooperBlack.png")

        self.resize(self.width, self.height)
        self.screen.fill(self.backgroundColor)
        pygame.display.set_caption(caption)

    def updateWindow(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pygame.display.update()
        self.resize(self.width, self.height)
        self.drawBoard()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h)
            for tileButton in self.tileButtons:
                if tileButton.isClicked():
                    buttonTile = tileButton.tile
                    self.drawRandomBug(buttonTile)
            pygame.display.update()


    def resize(self, newWidth, newHeight):
        self.screen = pygame.display.set_mode((newWidth, newHeight), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.fill(self.backgroundColor)
        self.width = newWidth
        self.height = newHeight
        self.xCenter = int(newWidth / 2)
        self.yCenter = int(newHeight / 2)
        newRadius = int((0.7 * newWidth / (2 * self.board.size + 1)) / (2 * self.cos30))
        newMargin = int(newRadius * self.marginRadiusRatio)
        if (newRadius * 2 * (self.board.size * 2 + 1) - self.board.size * (2 * (newRadius + newMargin) * self.cos30 * self.cos60)) > newHeight:
            newRadius = int((newHeight / (4 * self.board.size + 1)) / (2 * self.sin30))
            newMargin = int(newRadius * self.marginRadiusRatio)
        self.tileRadius = newRadius
        self.margin = newMargin
        self.bugScale = (self.bugRadiusRatio * newRadius / self.antWhite.get_width())
        self.drawBoard()

    def drawHex(self, xCenter, yCenter, radius, color):
        vertices = []
        for i in range(6):
            x = xCenter + radius * math.cos(self.tiltAngle + math.pi * 2 * i / 6)
            y = yCenter + radius * math.sin(self.tiltAngle + math.pi * 2 * i / 6)
            vertices.append([int(x), int(y)])
        return pygame.draw.polygon(self.screen, color, vertices)

    def transformToRealCoordinates(self, pole, xCenter, yCenter, tileRadius, margin):
        x = int(xCenter + (tileRadius + margin) * self.cos30 * (pole.s - pole.q))
        y = int(yCenter + (tileRadius + margin) * (self.sin30 * (pole.q + pole.s) - pole.r))
        return (x, y)

    def drawBoard(self):
        self.tileButtons = []
        for pole in self.board.iterList:
            coordinates = self.transformToRealCoordinates(pole, self.xCenter, self.yCenter, self.tileRadius, self.margin)
            color = None
            if pole.hatchery:
                color = self.hatcheryColor
            elif pole.resources:
                color = self.resourcesColor
            else:
                color = self.tileColor
            tileButton = TileButton(pole, self.drawHex(coordinates[0], coordinates[1], self.tileRadius, color))
            if pole.bug is not None:
                self.drawBug(pole.bug, pole)
            self.tileButtons.append(tileButton)


    def createNewGameWindow(self):
        pygame.init()

    def drawBug(self, bug, tile):
        coordinates = self.transformToRealCoordinates(tile, self.xCenter, self.yCenter, self.tileRadius, self.margin)
        image = None
        if isinstance(bug, Konik):
            if bug.side == 'W':
                image = self.grasshooperWhite
            elif bug.side == 'B':
                image = self.grasshooperBlack
        elif isinstance(bug, Mrowka):
            if bug.side == 'W':
                image = self.antWhite
            elif bug.side == 'B':
                image = self.antBlack
        elif isinstance(bug, Pajak):
            if bug.side == 'W':
                image = self.spiderWhite
            elif bug.side == 'B':
                image = self.spiderBlack
        elif isinstance(bug, Zuk):
            if bug.side == 'W':
                image = self.beetleWhite
            elif bug.side == 'B':
                image = self.beetleBlack
        if image is None:
            print("there is no image for ", type(bug), "bug, or bug doesn't have valid side assigned")
            return
        image = pygame.transform.smoothscale(image.convert_alpha(), (int(image.get_width() * self.bugScale), int(image.get_height() * self.bugScale)))
        self.screen.blit(image, (int(coordinates[0] - image.get_width() / 2), int(coordinates[1] - image.get_height() / 2)))

    # Useless test function
    def drawRandomBug(self, tile):
        x = randrange(8)
        bug = None
        if x == 0:
            bug = Zuk("W")
        elif x == 1:
            bug = Zuk("B")
        elif x == 2:
            bug = Pajak("W")
        elif x == 3:
            bug = Pajak("B")
        elif x == 4:
            bug = Mrowka("W")
        elif x == 5:
            bug = Mrowka("B")
        elif x == 6:
            bug = Konik("W")
        elif x == 7:
            bug = Konik("B")
        self.drawBug(bug, tile)

    def updateBoard(self, board):
        self.board = board
        self.drawBoard()


if __name__ == '__main__':
    board = Plansza()
    ui = UI(board)
    ui.updateWindow()

