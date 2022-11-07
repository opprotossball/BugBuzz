import pygame
import math
from FrontEnd.TileButton import TileButton
from pygame.locals import *


class Display:

    def __init__(self, game_master, max_fps=40, caption='Bug Buzz', background_color=(80, 80, 80), tile_color=(153, 153, 153), resources_color=(0, 160, 0), hatchery_color=(150, 45, 45), highlighted_color=(81, 210, 252), selected_color=(255, 225, 64)):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.backgroundColor = background_color
        self.tileColor = tile_color
        self.resourcesColor = resources_color
        self.hatcheryColor = hatchery_color
        self.highlightedColor = highlighted_color
        self.selectedColor = selected_color
        self.max_fps = max_fps

        self.DEFAULT_WIDTH = 1600
        self.DEFAULT_HEIGHT = 900
        self.TILE_RADIUS = 50
        self.TILE_MARGIN = 5
        self.X_BOARD_CENTER = 759
        self.Y_BOARD_CENTER = 480

        self.font23 = pygame.font.Font("./FrontEnd/Assets/Fonts/ANTQUAB.TTF", 40)
        self.img = self.font23.render('White\'s combat phase', True, (255, 255, 255))

        self.screen = None
        self.window_scale = 1
        self.gameMaster = game_master
        self.tiltAngle = math.pi / 2

        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.cos60 = math.cos(math.pi / 3)
        self.sin60 = math.sin(math.pi / 3)
        self.tileButtons = []
        self.highlightedTiles = []

        self.beetleWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/BeetleWhite.png"), True, False)
        self.beetleBlack = pygame.image.load("./FrontEnd/Assets/Bugs/BeetleBlack.png")
        self.spiderWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/SpiderWhite.png"), True, False)
        self.spiderBlack = pygame.image.load("./FrontEnd/Assets/Bugs/SpiderBlack.png")
        self.antWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/AntWhite.png"), True, False)
        self.antBlack = pygame.image.load("./FrontEnd/Assets/Bugs/AntBlack.png")
        self.grasshooperWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/GrasshooperWhite.png"), True, False)
        self.grasshooperBlack = pygame.image.load("./FrontEnd/Assets/Bugs/GrasshooperBlack.png")
        pygame.display.set_caption(caption)



    def updateWindow(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                pass
        self.screen = pygame.display.set_mode((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.fill(self.backgroundColor)
        if self.gameMaster.ui is not None:
            self.gameMaster.ui.getInput()
            self.drawSelected()
            self.highlight()
        self.draw_tiles()
        self.drawBugs()
        self.drawButtons(self.gameMaster.ui.hatchButtons)
        self.screen.blit(self.img, (50, 50))
        pygame.display.flip()
        self.clock.tick(self.max_fps)

    def draw_hex(self, x_center, y_center, radius, color):
        vertices = []
        for i in range(6):
            x = x_center + radius * math.cos(self.tiltAngle + math.pi * 2 * i / 6)
            y = y_center + radius * math.sin(self.tiltAngle + math.pi * 2 * i / 6)
            vertices.append([int(x), int(y)])
        return pygame.draw.polygon(self.screen, color, vertices)

    def transform_to_real_coordinates(self, pole):
        x = int(self.X_BOARD_CENTER + (self.TILE_RADIUS + self.TILE_MARGIN) * self.cos30 * (pole.s - pole.q))
        y = int(self.Y_BOARD_CENTER + (self.TILE_RADIUS + self.TILE_MARGIN) * (self.sin30 * (pole.q + pole.s) - pole.r))
        return x, y

    def draw_tiles(self):
        tile_buttons = []
        for pole in self.gameMaster.board.iterList:
            coordinates = self.transform_to_real_coordinates(pole)
            if pole.is_white_hatchery or pole.is_black_hatchery:
                color = self.hatcheryColor
            elif pole.resources:
                color = self.resourcesColor
            else:
                color = self.tileColor
            tile_button = TileButton(pole, self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, color))
            tile_buttons.append(tile_button)
        if self.gameMaster.ui is not None:
            self.gameMaster.ui.setTileButtons(tile_buttons)

    def drawBugs(self):
        for bug in self.gameMaster.BlackPlayer.bugList:
            self.drawBug(bug, bug.field)
        for bug in self.gameMaster.WhitePlayer.bugList:
            self.drawBug(bug, bug.field)

    def drawButtons(self, buttons):
        x = 40
        y = 275
        for button in buttons:
            button.draw(self.screen, x, y)
            y += 144

    def drawBug(self, bug, tile):
        coordinates = self.transform_to_real_coordinates(tile)
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
        #image = pygame.transform.smoothscale(image, (int(image.get_width() * self.bugScale), int(image.get_height() * self.bugScale)))
        self.screen.blit(image, (int(coordinates[0] - image.get_width() / 2), int(coordinates[1] - image.get_height() / 2)))

    def highlight(self):
        for tile in self.highlightedTiles:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.highlightedColor)

    def drawSelected(self):
        tile = self.gameMaster.ui.selected_tile
        if tile is not None:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.selectedColor)
