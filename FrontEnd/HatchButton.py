import pygame

class HatchButton:
    clickedLeft = False

    def __init__(self, image, imageSelected, bugShortName):
        self.image = image
        self.imageSelected = imageSelected
        self.bugShortName = bugShortName
        self.selected = False
        self.rect = None

    def draw(self, surface, x, y, scale):
        if self.selected:
            image = self.imageSelected
        else:
            image = self.image
        image = pygame.transform.smoothscale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        surface.blit(image, (x, y))

    def isClickedLeft(self):
        if self.rect == None:
            return False
        action = False
        mousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 0:
            HatchButton.clickedLeft = False
        elif self.rect.collidepoint(mousePosition) and not HatchButton.clickedLeft:
            self.selected = True
            HatchButton.clickedLeft = True
            action = True
        elif not self.rect.collidepoint(mousePosition):
            self.selected = False
        return action
