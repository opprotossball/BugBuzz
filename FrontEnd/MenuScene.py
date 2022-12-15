import pygame.image
import webbrowser

from BackEnd.GameMechanic.HumanPlayer import HumanPlayer
from FrontEnd.Button import Button
from FrontEnd.GameScene import GameScene
from FrontEnd.Scene import Scene
from Util.PlayerEnum import PlayerEnum


class MenuScene(Scene):
    def __init__(self, game_master):
        self.main_surface = None
        self.window_scale = None
        self.gm = game_master
        self.background = pygame.image.load("./FrontEnd/Assets/Menu/Menu.png")
        self.new_game_button_image = pygame.image.load("./FrontEnd/Assets/Menu/StartGameButton.png")
        self.how_to_play_button_image = pygame.image.load("./FrontEnd/Assets/Menu/HowToPlayButton.png")
        self.about_project_button_image = pygame.image.load("./FrontEnd/Assets/Menu/AboutProjectButton.png")

        self.about_url = "https://github.com/StanislawMalinski/RobaleProject/wiki"
        self.how_to_url = "https://github.com/StanislawMalinski/RobaleProject/blob/main/ProjectInforamtion/GameInstructionPL.pdf"

        self.new_game_button = Button(self.new_game_button_image, keyboard_key=pygame.K_RETURN)
        self.how_to_play_button = Button(self.how_to_play_button_image)
        self.about_project_button = Button(self.about_project_button_image)

    def on_update(self, surface, window_scale):
        self.main_surface = surface
        self.window_scale = window_scale
        surface.blit(self.background, (0, 0))

        self.new_game_button.draw(surface, 480, 325)
        self.how_to_play_button.draw(surface, 480, 472)
        self.about_project_button.draw(surface, 480, 619)

        self.new_game_button.set_window_scale(window_scale)
        self.how_to_play_button.set_window_scale(window_scale)
        self.about_project_button.set_window_scale(window_scale)

        if self.new_game_button.is_clicked_left():
            self.gm.display.set_scene(GameScene(self.gm))
            self.gm.new_game(HumanPlayer(self.gm, PlayerEnum.B), HumanPlayer(self.gm, PlayerEnum.C))

        if self.how_to_play_button.is_clicked_left():
            webbrowser.open(self.how_to_url)

        if self.about_project_button.is_clicked_left():
            webbrowser.open(self.about_url)
