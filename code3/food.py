import pygame
import random
import math
from pygame.math import Vector2
from setting import TILE_SIZE

class Food(pygame.sprite.Sprite):
    def __init__(self, groups, snake, valid_positions, mode):
        super().__init__(groups)

        self.mode = mode
        image_file = 'data/images/foods/food1.png' if mode == 'easy' else 'data/images/foods/food2.png'
        spritesheet = pygame.image.load(image_file).convert_alpha()
        
        # 4 frames xếp theo lưới 2 cột x 2 hàng
        self.frames = []
        frame_size = 50
        positions = [
            (0, 0),    # Frame 0: cột 0, hàng 0
            (50, 0),   # Frame 1: cột 1, hàng 0
            (0, 50),   # Frame 2: cột 0, hàng 1
            (50, 50),  # Frame 3: cột 1, hàng 1
        ]
        
        for x, y in positions:
            frame_rect = pygame.Rect(x, y, frame_size, frame_size)
            frame = spritesheet.subsurface(frame_rect)
            frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
            self.frames.append(frame)
        
        # Animation properties
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        
        self.image = self.frames[0]
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
    def update(self, dt):
        """Cập nhật animation"""
        # Animation từ spritesheet
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
