import pygame


class TileButton:

    clickedLeft = False
    clickedRight = False

    def __init__(self, pole, polygon):
        self.tile = pole
        self.polygon = polygon
        self.window_scale = 1

    def is_clicked_left(self):
        if pygame.mouse.get_pressed()[0] == 0:
            TileButton.clickedLeft = False
        elif self.is_hovered() and not TileButton.clickedLeft:
            TileButton.clickedLeft = True
            return True
        else:
            return False

    def is_clicked_right(self):
        if pygame.mouse.get_pressed()[2] == 0:
            TileButton.clickedRight = False
        elif self.is_hovered() and not TileButton.clickedRight:
            TileButton.clickedRight = True
            return True
        else:
            return False

    def is_hovered(self):
        position = pygame.mouse.get_pos()
        if self.polygon.collidepoint((position[0] / self.window_scale, position[1] / self.window_scale)):
            return True

    def set_window_scale(self, scale):
        self.window_scale = scale
