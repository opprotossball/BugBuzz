import pygame
import math
from FrontEnd.TileButton import TileButton
from pygame.locals import *


class Display:

    def __init__(self, game_master, max_fps=40, caption='Bug Buzz', background_color=(80, 80, 80), tile_color=(153, 153, 153), resources_color=(29, 122, 29), hatchery_color=(150, 45, 45), highlighted_color=(81, 210, 252), selected_color=(255, 225, 64)):
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
        self.TILE_RADIUS = 58
        self.TILE_MARGIN = 4
        self.X_BOARD_CENTER = 759
        self.Y_BOARD_CENTER = 450
        self.BUG_RADIUS_RATIO = 1.4
        self.MIN_SCALE = 0.3

        self.width = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.font40 = pygame.font.Font("./FrontEnd/Assets/Fonts/ANTQUAB.TTF", 40)
        self.font30 = pygame.font.Font("./FrontEnd/Assets/Fonts/ANTQUAB.TTF", 30)

        self.main_surface = pygame.Surface((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))
        self.screen = pygame.display.set_mode((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)

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
                self.resize(event.size)
        self.main_surface.fill(self.backgroundColor)
        self.draw_tiles()
        if self.gameMaster.ui is not None:
            self.gameMaster.ui.getInput()
            self.highlight()
            self.drawSelected()
            self.drawButtons()
            self.show_phase_title()
            self.show_number_of_bugs_available()
            self.show_number_of_resources()
        self.drawBugs()
        self.show_combat_results()
        if self.window_scale != 1:
            surface = pygame.transform.smoothscale(self.main_surface, (self.width, self.height))
        else:
            surface = self.main_surface
        self.screen.blit(surface, (0, 0))

        pygame.display.flip()
        self.clock.tick(self.max_fps)

    def resize(self, size):
        new_width, new_height = size
        if abs(self.width - new_width) > abs(self.height - new_height):
            scale = new_width / self.DEFAULT_WIDTH
        else:
            scale = new_height / self.DEFAULT_HEIGHT
        if scale < self.MIN_SCALE:
            scale = self.MIN_SCALE
        self.width = int(self.DEFAULT_WIDTH * scale)
        self.height = int(self.DEFAULT_HEIGHT * scale)
        self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.window_scale = scale

    def draw_hex(self, x_center, y_center, radius, color):
        vertices = []
        for i in range(6):
            x = x_center + radius * math.cos(self.tiltAngle + math.pi * 2 * i / 6)
            y = y_center + radius * math.sin(self.tiltAngle + math.pi * 2 * i / 6)
            vertices.append([int(x), int(y)])
        return pygame.draw.polygon(self.main_surface, color, vertices)

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
            tile_button.set_window_scale(self.window_scale)
            tile_buttons.append(tile_button)
        if self.gameMaster.ui is not None:
            self.gameMaster.ui.setTileButtons(tile_buttons)

    def drawBugs(self):
        for bug in self.gameMaster.BlackPlayer.bugList:
            self.drawBug(bug, bug.field)
        for bug in self.gameMaster.WhitePlayer.bugList:
            self.drawBug(bug, bug.field)

    def drawButtons(self):
        x = 40
        y = 275
        for button in self.gameMaster.ui.hatch_buttons:
            button.draw(self.main_surface, x, y)
            button.set_window_scale(self.window_scale)
            y += 144
        self.gameMaster.ui.end_phase_button.set_window_scale(self.window_scale)
        self.gameMaster.ui.end_phase_button.draw(self.main_surface, 1300, 805)

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
        self.main_surface.blit(image, (int(coordinates[0] - image.get_width() / 2), int(coordinates[1] - image.get_height() / 2)))

    def highlight(self):
        for tile in self.highlightedTiles:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.highlightedColor)


    def drawSelected(self):
        tile = self.gameMaster.ui.selected_tile
        if tile is not None:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.selectedColor)

    def show_phase_title(self):
        turn = self.gameMaster.turn
        text, color = self.gameMaster.ui.get_phase_title()
        title = self.font40.render(text, True, color)
        self.main_surface.blit(title, (int(1350 - title.get_width() / 2), int(75 - title.get_height() / 2)))

    def show_number_of_bugs_available(self):
        x = 170
        y = 310
        dictionary, color = self.gameMaster.ui.get_count_of_bugs_available()
        for key in dictionary:
            text = self.font40.render("x{}".format(dictionary[key]), True, color)
            self.main_surface.blit(text, (x, y))
            y += 144

    def show_number_of_resources(self):
        x = 85
        y = 80
        resources, color = self.gameMaster.ui.get_number_of_resources()
        text = self.font40.render("{}".format(resources), True, color)
        self.draw_hex(x, y, 55, self.resourcesColor)
        self.main_surface.blit(text, (int(x - text.get_width() / 2), int(y - text.get_height() / 2)))

    def show_combat_results(self):
        message, color = self.gameMaster.ui.get_combat_results()
        if message is None:
            return
        lines = message.split("\n")
        x = 1350
        y = 175
        for line in lines:
            text = self.font30.render(line, True, color)
            self.main_surface.blit(text, (int(x - text.get_width() / 2), int(y - text.get_height() / 2)))
            y += int(text.get_height() * 1.3)
