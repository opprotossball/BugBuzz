import pygame.image
import webbrowser

from AI_module import AproxBotDefaultWeights
from AI_module.BasicAprox import BasicAprox
from AI_module.RandomBot import RandomBot
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
        new_game_button_image = pygame.image.load("./FrontEnd/Assets/Menu/StartGameButton.png")
        how_to_play_button_image = pygame.image.load("./FrontEnd/Assets/Menu/HowToPlayButton.png")
        about_project_button_image = pygame.image.load("./FrontEnd/Assets/Menu/AboutProjectButton.png")
        play_online_button = pygame.image.load("./FrontEnd/Assets/Menu/PlayOnlineButton.png")

        self.about_url = "https://github.com/StanislawMalinski/RobaleProject/wiki"
        self.how_to_url = "https://github.com/StanislawMalinski/RobaleProject/blob/main/ProjectInforamtion/GameInstructionPL.pdf"

        self.new_game_button = Button(new_game_button_image, keyboard_key=pygame.K_RETURN)
        self.play_online_button = Button(play_online_button)
        self.how_to_play_button = Button(how_to_play_button_image)
        self.about_project_button = Button(about_project_button_image)

    def on_update(self, surface, window_scale):
        self.main_surface = surface
        self.window_scale = window_scale
        surface.blit(self.background, (0, 0))

        self.new_game_button.draw(surface, 480, 280)
        self.play_online_button.draw(surface, 480, 408)
        self.how_to_play_button.draw(surface, 480, 537)
        self.about_project_button.draw(surface, 480, 665)

        self.new_game_button.set_window_scale(window_scale)
        self.how_to_play_button.set_window_scale(window_scale)
        self.about_project_button.set_window_scale(window_scale)
        self.play_online_button.set_window_scale(window_scale)

        if self.new_game_button.is_clicked_left():
            self.gm.display.set_scene(GameScene(self.gm))
            self.gm.new_game(HumanPlayer(self.gm, PlayerEnum.B), BasicAprox(self.gm, PlayerEnum.C, AproxBotDefaultWeights.default_weights))

        if self.play_online_button.is_clicked_left():
            self.gm.playing_online = True

        if self.how_to_play_button.is_clicked_left():
            webbrowser.open(self.how_to_url)

        if self.about_project_button.is_clicked_left():
            webbrowser.open(self.about_url)
