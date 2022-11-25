import pygame

class TileButton:
    clickedLeft = False
    clickedRight = False

    def __init__(self, pole, polygon):
        self.tile = pole
        self.polygon = polygon
        self.window_scale = 1

    def isClickedLeft(self):
        if pygame.mouse.get_pressed()[0] == 0:
            TileButton.clickedLeft = False
        elif self.isHovered() and not TileButton.clickedLeft:
            TileButton.clickedLeft = True
            return True
        else:
            return False

    def isClickedRight(self):
        if pygame.mouse.get_pressed()[2] == 0:
            TileButton.clickedRight = False
        elif self.isHovered() and not TileButton.clickedRight:
            TileButton.clickedRight = True
            return True
        else:
            return False

    def isHovered(self):
        position = pygame.mouse.get_pos()
        if self.polygon.collidepoint((position[0] / self.window_scale, position[1] / self.window_scale)):
            return True

    def set_window_scale(self, scale):
        self.window_scale = scale
