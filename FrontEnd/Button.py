import pygame


class Button:

    def __init__(self, image, imageSelected=None, bugShortName=None):
        self.image = image
        self.imageSelected = imageSelected
        self.bugShortName = bugShortName
        self.selected = False
        self.rect = None
        self.clickedLeft = False

    def draw(self, surface, x, y):
        if self.selected and self.imageSelected is not None:
            image = self.imageSelected.convert_alpha()
        else:
            image = self.image.convert_alpha()
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        surface.blit(image, (x, y))

    def isClickedLeft(self):
        if self.rect is None:
            return False
        action = False
        mouse_position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 0:
            self.clickedLeft = False
        elif self.rect.collidepoint(mouse_position) and not self.clickedLeft:
            self.selected = True
            self.clickedLeft = True
            action = True
        elif not self.rect.collidepoint(mouse_position):
            self.selected = False
            action = False
        return action

    def isSelected(self):
        return self.selected
