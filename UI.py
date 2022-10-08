import pygame
import math
from Plansza import Plansza


class UI:

    def __init__(self, windowWidth, windowHeight):
        self.backgroundColor = (80, 80, 80)
        self.tileColor = (190, 190, 190)
        self.resourcesColor = (0, 160, 0)
        self.hatcheryColor = (150, 45, 45)

        self.width = windowWidth
        self.height = windowHeight
        self.running = True
        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.tiltAngle = math.pi / 2
        pygame.display.set_caption('Robale')
        self.screen.fill(self.backgroundColor)

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

    def drawBoard(self, plansza, xCenter, yCenter, tileRadius, marigin):
        for pole in plansza.iterList:
            coordinates = self.transformToRealCoordinates(pole, xCenter, yCenter, tileRadius, marigin)
            if pole.hatchery:
                self.drawHex(coordinates[0], coordinates[1], tileRadius, self.hatcheryColor)
            elif pole.resources:
                self.drawHex(coordinates[0], coordinates[1], tileRadius, self.resourcesColor)
            else:
                self.drawHex(coordinates[0], coordinates[1], tileRadius, self.tileColor)


if __name__ == '__main__':
    pygame.init()
    ui = UI(1000, 800)
    pl = Plansza()
    ui.drawBoard(pl, 500, 400, 40, 3)
    ui.updateWindow()



