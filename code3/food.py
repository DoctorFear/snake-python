import pygame
import random
from pygame.math import Vector2
from setting import TILE_SIZE, GAME_WIDTH, GAME_HEIGHT

class Food(pygame.sprite.Sprite):
    def __init__(self, groups, snake, valid_positions):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))  # Màu đỏ cho thức ăn
        self.rect = self.image.get_rect()
        self.snake = snake
        self.valid_positions = valid_positions  # Danh sách các vị trí hợp lệ từ bản đồ
        self.respawn(snake)

    def respawn(self, snake):
        while True:
            # Chọn ngẫu nhiên từ danh sách vị trí hợp lệ
            pos = random.choice(self.valid_positions)
            self.rect.topleft = (pos.x * TILE_SIZE, pos.y * TILE_SIZE)
            if pos not in snake.body:
                break