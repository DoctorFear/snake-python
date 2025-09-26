import pygame
from setting import TILE_SIZE

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, groups=None):
        super().__init__(groups if groups is not None else ())
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)