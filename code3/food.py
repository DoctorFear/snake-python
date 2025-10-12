import pygame
import random
import math
from pygame.math import Vector2
from setting import TILE_SIZE

class Food(pygame.sprite.Sprite):
    def __init__(self, groups, snake, valid_positions):
        super().__init__(groups)
        self.base_image = pygame.image.load("data/images/food.png").convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (TILE_SIZE, TILE_SIZE))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

        self.snake = snake
        self.valid_positions = valid_positions

        self.time = 0
        self.respawn(snake)

    def respawn(self, snake):
        while True:
            pos = random.choice(self.valid_positions)
            self.rect.topleft = (pos.x * TILE_SIZE, pos.y * TILE_SIZE)
            if pos not in snake.body:
                break

    #Glow effect cho food
    def update(self):
        # tăng thời gian để tạo hiệu ứng dao động ánh sáng
        self.time += 0.1

        # phát sáng nhẹ bằng sin wave
        glow = (math.sin(self.time * 2) + 1) / 2  
        brightness = 180 + int(glow * 75)         

        # tạo overlay sáng lên
        self.image = self.base_image.copy()
        overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        overlay.fill((brightness, brightness, brightness, 60)) 
        self.image.blit(overlay, (0, 0))
