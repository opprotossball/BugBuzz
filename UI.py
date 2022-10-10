import pygame
from pygame.locals import *
import math
from Plansza import Plansza
from Pole import Pole
from Robal import *
from random import randrange


class TileButton:

    def __init__(self, pole, polygon):
        self.tile = pole
        self.polygon = polygon
        self.clicked = False

    def isClicked(self):
        mousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        elif self.polygon.collidepoint(mousePosition) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            return True
        else:
            return False


class UI:

    def __init__(self, windowWidth, windowHeight, tileRadius, margin):
        self.backgroundColor = (80, 80, 80)
        self.tileColor = (153, 153, 153)
        self.resourcesColor = (0, 160, 0)
        self.hatcheryColor = (150, 45, 45)

        pygame.display.set_caption('Robale')
        self.xCenter = int(windowWidth / 2)
        self.yCenter = int(windowHeight / 2)
        self.tiltAngle = math.pi / 2

        self.margin = margin
        self.tileRadius = tileRadius
        self.width = windowWidth
        self.height = windowHeight
        self.running = True
        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.cos60 = math.cos(math.pi / 3)
        self.sin60 = math.sin(math.pi / 3)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.backgroundColor)
        self.tileButtons = []

        self.beetleWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/BeetleWhite.png"), True, False)
        self.beetleBlack = pygame.image.load("Assets/Bugs/BeetleBlack.png")
        self.spiderWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/SpiderWhite.png"), True, False)
        self.spiderBlack = pygame.image.load("Assets/Bugs/SpiderBlack.png")
        self.antWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/AntWhite.png"), True, False)
        self.antBlack = pygame.image.load("Assets/Bugs/AntBlack.png")
        self.grasshooperWhite = pygame.transform.flip(pygame.image.load("Assets/Bugs/GrasshooperWhite.png"), True, False)
        self.grasshooperBlack = pygame.image.load("Assets/Bugs/GrasshooperBlack.png")

    def updateWindow(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for tileButton in self.tileButtons:
                if tileButton.isClicked():
                    tile = tileButton.tile
                    self.drawRandomBug(tile)
            pygame.display.update()

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

    def drawBoard(self, plansza):
        for pole in plansza.iterList:
            coordinates = self.transformToRealCoordinates(pole, self.xCenter, self.yCenter, self.tileRadius, self.margin)
            color = None
            if pole.hatchery:
                color = self.hatcheryColor
            elif pole.resources:
                color = self.resourcesColor
            else:
                color = self.tileColor
            tileButton = TileButton(pole, self.drawHex(coordinates[0], coordinates[1], self.tileRadius, color))
            self.tileButtons.append(tileButton)

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


if __name__ == '__main__':
    screenWidth = 1920
    screenHeight = 1080
    pygame.init()
    ui = UI(screenWidth, screenHeight, 60, 4.5)
    board = Plansza()
    ui.drawBoard(board)
    ui.updateWindow()
