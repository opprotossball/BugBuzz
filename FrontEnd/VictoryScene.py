import pygame

from FrontEnd.Button import Button
from FrontEnd.MenuScene import MenuScene
from FrontEnd.Scene import Scene
from Util.PlayerEnum import PlayerEnum


class VictoryScene(Scene):

    def __init__(self, gm, side):
        self.gm = gm
        self.background = None
        self.button_image = None
        if side == PlayerEnum.B:
            self.background = pygame.image.load("./FrontEnd/Assets/VictoryScene/WhiteVictory.png")
            button_image = pygame.image.load("./FrontEnd/Assets/VictoryScene/WhiteHomeButton.png")
        elif side == PlayerEnum.C:
            self.background = pygame.image.load("./FrontEnd/Assets/VictoryScene/BlackVictory.png")
            button_image = pygame.image.load("./FrontEnd/Assets/VictoryScene/BlackHomeButton.png")
        self.home_button = Button(button_image)

    def on_update(self, surface, window_scale):
        surface.blit(self.background, (0, 0))

        self.home_button.draw(surface, 1402, 702)
        self.home_button.set_window_scale(self.gm.display.window_scale)

        if self.home_button.is_clicked_left():
            self.gm.display.set_scene(MenuScene(self.gm))
