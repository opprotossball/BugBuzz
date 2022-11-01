import pygame

class TileButton:
    clickedLeft = False
    clickedRight = False

    def __init__(self, pole, polygon):
        self.tile = pole
        self.polygon = polygon

    def isClickedLeft(self):
        if pygame.mouse.get_pressed()[0] == 0:
            TileButton.clickedLeft = False
        elif self.isHovered() and pygame.mouse.get_pressed()[0] == 1 and not TileButton.clickedLeft:
            TileButton.clickedLeft = True
            return True
        else:
            return False

    def isClickedRight(self):
        if pygame.mouse.get_pressed()[2] == 0:
            TileButton.clickedRight = False
        elif self.isHovered() and pygame.mouse.get_pressed()[2] == 1 and not TileButton.clickedRight:
            TileButton.clickedRight = True
            return True
        else:
            return False

    def isHovered(self):
        mousePosition = pygame.mouse.get_pos()
        if self.polygon.collidepoint(mousePosition):
            return True
