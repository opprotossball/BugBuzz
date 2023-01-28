import pygame
import math

from BackEnd.GameObjects.Robal import RobalEnum
from FrontEnd.Scene import Scene
from FrontEnd.TileButton import TileButton
from Util.PlayerEnum import PlayerEnum


class GameScene(Scene):

    def __init__(self, game_master, background_color=(80, 80, 80), tile_color=(153, 153, 153), resources_color=(29, 122, 29), hatchery_color=(150, 45, 45), highlighted_color=(81, 210, 252), selected_color=(255, 225, 64), attacked_color=(150, 45, 45)):
        self.backgroundColor = background_color
        self.tileColor = tile_color
        self.resourcesColor = resources_color
        self.hatcheryColor = hatchery_color
        self.highlightedColor = highlighted_color
        self.selectedColor = selected_color
        self.attacked_color = attacked_color

        self.TILE_RADIUS = 58
        self.TILE_MARGIN = 4
        self.X_BOARD_CENTER = 759
        self.Y_BOARD_CENTER = 450

        self.font40 = pygame.font.Font("./FrontEnd/Assets/Fonts/ANTQUAB.TTF", 40)
        self.font35 = pygame.font.Font("./FrontEnd/Assets/Fonts/ANTQUAB.TTF", 35)
        self.font30 = pygame.font.Font("./FrontEnd/Assets/Fonts/ANTQUAB.TTF", 30)

        self.gameMaster = game_master
        self.tiltAngle = math.pi / 2

        self.cos30 = math.cos(math.pi / 6)
        self.sin30 = math.sin(math.pi / 6)
        self.cos60 = math.cos(math.pi / 3)
        self.sin60 = math.sin(math.pi / 3)
        self.tileButtons = []
        self.highlightedTiles = []

        self.highlighted_by_online_opponent = []
        self.army_attacked_by_online_opponent = None
        self.online_opponent_leader = None
        self.online_opponent_rolls = []
        self.online_opponent_kills = 0

        self.main_surface = None
        self.window_scale = None

        self.beetleWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/BeetleWhite.png"), True, False)
        self.beetleBlack = pygame.image.load("./FrontEnd/Assets/Bugs/BeetleBlack.png")
        self.spiderWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/SpiderWhite.png"), True, False)
        self.spiderBlack = pygame.image.load("./FrontEnd/Assets/Bugs/SpiderBlack.png")
        self.antWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/AntWhite.png"), True, False)
        self.antBlack = pygame.image.load("./FrontEnd/Assets/Bugs/AntBlack.png")
        self.grasshooperWhite = pygame.transform.flip(pygame.image.load("./FrontEnd/Assets/Bugs/GrasshooperWhite.png"), True, False)
        self.grasshooperBlack = pygame.image.load("./FrontEnd/Assets/Bugs/GrasshooperBlack.png")

    def on_update(self, surface, window_scale):
        self.main_surface = surface
        self.window_scale = window_scale
        surface.fill(self.backgroundColor)
        self.draw_tiles()

        if self.gameMaster.ui is not None:
            self.gameMaster.ui.get_input()
            self.highlight()
            self.draw_selected()
            self.draw_buttons()
            self.show_phase_title()
            self.show_number_of_bugs_available()
            self.show_number_of_resources()
            if not self.show_opponent_combat_results():
                self.show_combat_results()
                self.show_stats()
                self.show_tip()
        self.draw_bugs()

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
            if pole.resources:
                color = self.resourcesColor
            else:
                color = self.tileColor
            tile_button = TileButton(pole, self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, color))
            tile_button.set_window_scale(self.window_scale)
            tile_buttons.append(tile_button)
        if self.gameMaster.ui is not None:
            self.gameMaster.ui.set_tile_buttons(tile_buttons)

    def draw_bugs(self):
        for bug in self.gameMaster.BlackPlayer.bugList:
            self.draw_bug(bug, bug.field)
        for bug in self.gameMaster.WhitePlayer.bugList:
            self.draw_bug(bug, bug.field)

    def draw_buttons(self):
        x = 40
        y = 275
        for button in self.gameMaster.ui.hatch_buttons:
            button.draw(self.main_surface, x, y)
            button.set_window_scale(self.window_scale)
            y += 144
        self.gameMaster.ui.end_phase_button.set_window_scale(self.window_scale)
        self.gameMaster.ui.resign_button.set_window_scale(self.window_scale)
        self.gameMaster.ui.end_phase_button.draw(self.main_surface, 1190, 735)
        self.gameMaster.ui.resign_button.draw(self.main_surface, 1190, 805)

    def draw_bug(self, bug, tile):
        coordinates = self.transform_to_real_coordinates(tile)
        image = None
        if bug.short_name == RobalEnum.K:
            if bug.side == PlayerEnum.B:
                image = self.grasshooperWhite
            elif bug.side == PlayerEnum.C:
                image = self.grasshooperBlack
        elif bug.short_name == RobalEnum.M:
            if bug.side == PlayerEnum.B:
                image = self.antWhite
            elif bug.side == PlayerEnum.C:
                image = self.antBlack
        elif bug.short_name == RobalEnum.P:
            if bug.side == PlayerEnum.B:
                image = self.spiderWhite
            elif bug.side == PlayerEnum.C:
                image = self.spiderBlack
        elif bug.short_name == RobalEnum.Z:
            if bug.side == PlayerEnum.B:
                image = self.beetleWhite
            elif bug.side == PlayerEnum.C:
                image = self.beetleBlack
        if image is None:
            print("there is no image for ", type(bug), "bug, or bug doesn't have valid side assigned")
            return
        self.main_surface.blit(image, (
        int(coordinates[0] - image.get_width() / 2), int(coordinates[1] - image.get_height() / 2)))

    def highlight(self):
        for tile in self.highlightedTiles:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.highlightedColor)
        for tile in self.highlighted_by_online_opponent:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.highlightedColor)
        for tile in self.highlighted_by_online_opponent:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.attacked_color)

    def draw_selected(self):
        tile = self.gameMaster.ui.selected_tile
        if tile is not None:
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.selectedColor)
        if self.online_opponent_leader is not None:
            tile = self.gameMaster.board.get_field(self.online_opponent_leader[0], self.online_opponent_leader[1])
            coordinates = self.transform_to_real_coordinates(tile)
            self.draw_hex(coordinates[0], coordinates[1], self.TILE_RADIUS, self.selectedColor)

    def show_phase_title(self):
        text, color = self.gameMaster.ui.get_phase_title()
        title = self.font40.render(text, True, color)
        self.main_surface.blit(title, (int(1310 - title.get_width() / 2), int(75 - title.get_height() / 2)))

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
        self.write_multiline_text_30(message, color, 1300, 175)

    def show_opponent_combat_results(self):  # should be moved to ui maybe
        if len(self.online_opponent_rolls) < 1:
            return False
        message = "Opponent rolled: {}\nThey may kill {} bug".format(self.online_opponent_rolls, self.online_opponent_kills)
        if self.online_opponent_kills > 1:
            message += "s"
        if self.gameMaster.ui.side == PlayerEnum.B:
            color = self.gameMaster.ui.BLACK
        else:
            color = self.gameMaster.ui.WHITE
        self.write_multiline_text_30(message, color, 1300, 175, align=True, title=True)
        return True

    def show_stats(self):
        message, color = self.gameMaster.ui.get_stats()
        self.write_multiline_text_30(message, color, 1300, 175, align=True, title=True)

    def show_tip(self):
        message, color = self.gameMaster.ui.get_tip_text()
        self.write_multiline_text_30(message, color, 1314, 700)

    def write_multiline_text_30(self, message, color, x, y, space_height_ratio=1.3, align=False, title=False):
        if message is None:
            return
        lines = message.split("\n")
        if title:
            text = self.font35.render(lines[0], True, color)
            self.main_surface.blit(text, (int(x - text.get_width() / 2), int(y - text.get_height() / 2)))
            y += int(text.get_height() * space_height_ratio)
            del lines[0]
        if align:
            text = self.font30.render(lines[0], True, color)
            x = int(x - text.get_width() / 2)
            self.main_surface.blit(text, (x, int(y - text.get_height() / 2)))
            y += int(text.get_height() * space_height_ratio)
            for line in lines[1:]:
                text = self.font30.render(line, True, color)
                self.main_surface.blit(text, (x, int(y - text.get_height() / 2)))
                y += int(text.get_height() * space_height_ratio)
        else:
            for line in lines:
                text = self.font30.render(line, True, color)
                self.main_surface.blit(text, (int(x - text.get_width() / 2), int(y - text.get_height() / 2)))
                y += int(text.get_height() * space_height_ratio)
