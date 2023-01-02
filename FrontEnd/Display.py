import pygame
from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE


class Display:
    def __init__(self, max_fps=40, caption='Bug Buzz'):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.max_fps = max_fps
        self.DEFAULT_WIDTH = 1600
        self.DEFAULT_HEIGHT = 900
        self.MIN_SCALE = 0.5

        self.width = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.window_scale = 1

        self.main_surface = pygame.Surface((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))

        info = pygame.display.Info()
        if self.DEFAULT_WIDTH > info.current_w:
            self.width = info.current_w * 4 / 5
            self.window_scale = self.width / self.DEFAULT_WIDTH
            self.height = self.DEFAULT_HEIGHT * self.window_scale
        if self.height > info.current_h:
            self.height = info.current_h * 4 / 5
            self.window_scale = self.height / self.DEFAULT_HEIGHT
            self.width = self.DEFAULT_WIDTH * self.window_scale

        self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption(caption)

    def set_scene(self, scene):
        self.scene = scene

    def update_window(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.size)

        self.scene.on_update(self.main_surface, self.window_scale)

        if self.window_scale != 1:
            surface = pygame.transform.smoothscale(self.main_surface, (self.width, self.height))
        else:
            surface = self.main_surface
        self.screen.blit(surface, (0, 0))

        pygame.display.flip()

    def resize(self, size):
        new_width, new_height = size
        if abs(self.width - new_width) > abs(self.height - new_height):
            scale = new_width / self.DEFAULT_WIDTH
        else:
            scale = new_height / self.DEFAULT_HEIGHT
        if scale < self.MIN_SCALE:
            scale = self.MIN_SCALE
        self.width = int(self.DEFAULT_WIDTH * scale)
        self.height = int(self.DEFAULT_HEIGHT * scale)
        self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.window_scale = scale
