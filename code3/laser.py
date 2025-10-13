import pygame
from pygame.math import Vector2
from setting import TILE_SIZE

class Laser(pygame.sprite.Sprite):
    """Class quản lý tia laser bắn từ enemy"""
    
    def __init__(self, start_pos, direction, game_width, game_height, speed=10):
        self.start_pos = start_pos.copy()
        self.direction = direction.copy()
        self.game_width = game_width
        self.game_height = game_height
        self.active = False
        self.speed = speed
        self.current_length = 0
        self.max_length = self._calculate_max_length()
        
        # Load sprite laser
        laser_img = pygame.image.load('data/images/laser.png').convert_alpha()
        
        # Frame 1: Đầu (0, 0, 50, 50)
        self.laser_head = laser_img.subsurface(pygame.Rect(0, 0, 50, 50))
        self.laser_head = pygame.transform.scale(self.laser_head, (TILE_SIZE, TILE_SIZE))
        
        # Frame 2: Thân (0, 50, 50, 50)
        self.laser_body = laser_img.subsurface(pygame.Rect(0, 50, 50, 50))
        self.laser_body = pygame.transform.scale(self.laser_body, (TILE_SIZE, TILE_SIZE))
        
        # Xoay theo hướng
        self.laser_head = self._rotate_image(self.laser_head, direction)
        self.laser_body = self._rotate_image(self.laser_body, direction)
    
    def _rotate_image(self, image, direction):
        """Xoay hình theo hướng laser"""
        if direction.x == -1:
            return pygame.transform.rotate(image, 180)
        elif direction.y == 1:
            return pygame.transform.rotate(image, -90)
        elif direction.y == -1:
            return pygame.transform.rotate(image, 90)
        return image
        
    def _calculate_max_length(self):
        """Tính độ dài tối đa"""
        current_pos = self.start_pos.copy()
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)
        
        length = 0
        while 0 <= current_pos.x < map_w and 0 <= current_pos.y < map_h:
            length += 1
            current_pos += self.direction
        return length
        
    def activate(self):
        self.active = True
        self.current_length = 0
    
    def update(self, dt):
        if self.active and self.current_length < self.max_length:
            self.current_length += self.speed * dt
            if self.current_length > self.max_length:
                self.current_length = self.max_length
    
    def get_laser_positions(self):
        if not self.active:
            return []
        
        positions = []
        pos = self.start_pos.copy()
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)
        
        for _ in range(int(self.current_length)):
            if 0 <= pos.x < map_w and 0 <= pos.y < map_h:
                positions.append(pos.copy())
                pos += self.direction
            else:
                break
        return positions
    
    def check_collision_with_body(self, body_list):
        if not self.active:
            return False
        
        laser_positions = self.get_laser_positions()
        for body_part in body_list:
            if body_part in laser_positions:
                return True
        return False
    
    def draw(self, surface, camera_offset=(0, 0)):
        if not self.active:
            return
        
        laser_positions = self.get_laser_positions()
        
        for i, pos in enumerate(laser_positions):
            x = pos.x * TILE_SIZE - camera_offset[0]
            y = pos.y * TILE_SIZE - camera_offset[1]
            
            # ✅ Phần tròn luôn ở cuối (đầu laser đang chạy)
            if i == len(laser_positions) - 1:
                surface.blit(self.laser_head, (x, y))
            else:
                surface.blit(self.laser_body, (x, y))