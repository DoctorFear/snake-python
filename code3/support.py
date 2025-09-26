import pygame
from os.path import join

def import_image(*path, alpha=True, format='png'):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()