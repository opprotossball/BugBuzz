import pygame

from FrontEnd.Button import Button
from FrontEnd.MenuScene import MenuScene
from FrontEnd.Scene import Scene


class LoadingScene(Scene):

    def __init__(self, gm):
        self.gm = gm
        self.background = pygame.image.load("./FrontEnd/Assets/LoadingScene/LoadingScreen.png")
        button_image = pygame.image.load("./FrontEnd/Assets/Buttons/WhiteHomeButton.png")
        self.home_button = Button(button_image)

    def on_update(self, surface, window_scale):
        surface.blit(self.background, (0, 0))

        self.home_button.draw(surface, 1402, 702)
        self.home_button.set_window_scale(self.gm.display.window_scale)

        if self.home_button.is_clicked_left():
            self.gm.playing_online = False
            self.gm.display.set_scene(MenuScene(self.gm))
