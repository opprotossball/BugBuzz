import pygame
import math
from Plansza import Plansza
from Pole import Pole
from Robal import *


class UI:

    def __init__(self, windowWidth, windowHeight, tileRadius, margin):
        self.backgroundColor = (80, 80, 80)
        self.tileColor = (153, 153, 153)
        self.resourcesColor = (0, 160, 0)
        self.hatcheryColor = (150, 45, 45)

        self.margin = margin
        self.tileRadius = tileRadius
        self.width = windowWidth
        self.height = windowHeight
        self.xCenter = int(windowWidth / 2)
        self.yCenter = int(windowHeight / 2)
        self.running = True
        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.tiltAngle = math.pi / 2
        pygame.display.set_caption('Robale')
        self.screen.fill(self.backgroundColor)

        self.beetleWhite = pygame.image.load("Assets/Bugs/BeetleWhite.png")
        self.beetleBlack = pygame.image.load("Assets/Bugs/BeetleBlack.png")
        self.spiderWhite = pygame.image.load("Assets/Bugs/SpiderWhite.png")
        self.spiderBlack = pygame.image.load("Assets/Bugs/SpiderBlack.png")
        self.antWhite = pygame.image.load("Assets/Bugs/AntWhite.png")
        self.antBlack = pygame.image.load("Assets/Bugs/AntBlack.png")
        self.grasshooperWhite = pygame.image.load("Assets/Bugs/GrasshooperWhite.png")
        self.grasshooperBlack = pygame.image.load("Assets/Bugs/GrasshooperBlack.png")


    def updateWindow(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()

    def drawHex(self, xCenter, yCenter, radius, color):
        vertices = []
        for i in range(6):
            x = xCenter + radius * math.cos(self.tiltAngle + math.pi * 2 * i / 6)
            y = yCenter + radius * math.sin(self.tiltAngle + math.pi * 2 * i / 6)
            vertices.append([int(x), int(y)])
        pygame.draw.polygon(self.screen, color, vertices)

    def transformToRealCoordinates(self, pole, xCenter, yCenter, tileRadius, margin):
        x = int(xCenter + (tileRadius + margin) * self.cos30 * (pole.s - pole.q))
        y = int(yCenter + (tileRadius + margin) * (self.sin30 * (pole.q + pole.s) - pole.r))
        return (x, y)

    def drawBoard(self, plansza):
        for pole in plansza.iterList:
            coordinates = self.transformToRealCoordinates(pole, self.xCenter, self.yCenter, self.tileRadius, self.margin)
            if pole.hatchery:
                self.drawHex(coordinates[0], coordinates[1], self.tileRadius, self.hatcheryColor)
            elif pole.resources:
                self.drawHex(coordinates[0], coordinates[1], self.tileRadius, self.resourcesColor)
            else:
                self.drawHex(coordinates[0], coordinates[1], self.tileRadius, self.tileColor)

    def drawBug(self, bug, tile):
        if isinstance(bug, Konik):
            self.screen.blit(self.grasshooperWhite, self.transformToRealCoordinates(tile, self.xCenter, self.yCenter, self.tileRadius, self.margin))
        elif isinstance(bug, Mrowka):
            self.screen.blit(self.antWhite, self.transformToRealCoordinates(tile, self.xCenter, self.yCenter, self.tileRadius, self.margin))
        elif isinstance(bug, Pajak):
            self.screen.blit(self.spiderWhite, self.transformToRealCoordinates(tile, self.xCenter, self.yCenter, self.tileRadius, self.margin))
        elif isinstance(bug, Zuk):
            self.screen.blit(self.beetleWhite, self.transformToRealCoordinates(tile, self.xCenter, self.yCenter, self.tileRadius, self.margin))


if __name__ == '__main__':
    screenWidth = 1920
    screenHeight = 1080
    pygame.init()
    ui = UI(screenWidth, screenHeight, 60, 4.5)
    board = Plansza()
    ui.drawBoard(board)
    p = Pole(2, 2, -4, -1)
    m = Mrowka(1)
    ui.drawBug(m, p)
    ui.updateWindow()
    pl = Plansza()
    pl.getPlansza()




