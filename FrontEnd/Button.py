import pygame


class Button:

    def __init__(self, image, imageSelected=None, selected_for_time=None, bugShortName=None, keyboard_key=None):  #selected_for_time should be in seconds
        self.image = image
        self.imageSelected = imageSelected
        self.bugShortName = bugShortName
        self.keyboard_key = keyboard_key
        self.selected = False
        self.rect = None
        self.clickedLeft = False
        self.key_pressed = False
        self.selected_for_time = selected_for_time * 1000 if selected_for_time is not None else None
        self.last_clicked_time = 0
        self.window_scale = 1

    def draw(self, surface, x, y):
        time = pygame.time.get_ticks()
        if self.selected and self.imageSelected is not None:
            if self.selected_for_time is not None:
                if time - self.last_clicked_time < self.selected_for_time:
                    image = self.imageSelected.convert_alpha()
                else:
                    image = self.image.convert_alpha()
            else:
                image = self.imageSelected.convert_alpha()
        else:
            image = self.image.convert_alpha()
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        surface.blit(image, (x, y))

    def is_clicked_left(self):

        if self.keyboard_key is not None:
            keys = pygame.key.get_pressed()
            if keys[self.keyboard_key]:
                if not self.key_pressed:
                    self.selected = True
                    self.key_pressed = True
                    self.last_clicked_time = pygame.time.get_ticks()
                    return True
            else:
                self.key_pressed = False

        if self.rect is None:
            return False

        action = False
        mouse_position = pygame.mouse.get_pos()
        position = (mouse_position[0] / self.window_scale, mouse_position[1] / self.window_scale)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clickedLeft = False
        elif self.rect.collidepoint(position) and not self.clickedLeft:
            self.selected = True
            self.clickedLeft = True
            action = True
            self.last_clicked_time = pygame.time.get_ticks()
        elif not self.rect.collidepoint(position):
            self.selected = False
            action = False
        return action

    def is_selected(self):
        return self.selected

    def set_window_scale(self, scale):
        self.window_scale = scale
