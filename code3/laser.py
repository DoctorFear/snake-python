import pygame
from pygame.math import Vector2
from setting import TILE_SIZE

class Laser(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction, game_width, game_height, mode, speed=10):
        self.start_pos = start_pos.copy() + direction * 0.5
        self.direction = direction.copy()
        self.game_width = game_width
        self.game_height = game_height
        self.active = False
        self.speed = speed
        self.current_length = 0
        self.max_length = self._calculate_max_length()
        
        # Load sprite laser
        self.mode = mode
        laser_img = 'data/images/lasers/laser1.png' if mode == 'easy' else 'data/images/lasers/laser2.png'
        spritesheet = pygame.image.load(laser_img).convert_alpha()
        
        # Frame 1: Đầu (0, 0, 50, 50)
        self.laser_head = spritesheet.subsurface(pygame.Rect(0, 0, 50, 50))
        self.laser_head = pygame.transform.scale(self.laser_head, (TILE_SIZE, TILE_SIZE))
        
        # Frame 2: Thân (0, 50, 50, 50)
        self.laser_body = spritesheet.subsurface(pygame.Rect(0, 50, 50, 50))
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
        """Tính độ dài tối đa của laser (số ô có thể đi qua)."""
        current_pos = self.start_pos.copy()
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)
        
        length = 0
        while 0 <= current_pos.x < map_w and 0 <= current_pos.y < map_h:
            # Kiểm tra trước khi bước tiếp
            next_pos = current_pos + self.direction
            if not (0 <= next_pos.x < map_w and 0 <= next_pos.y < map_h):
                break
            length += 1
            current_pos = next_pos
        return length
        
    def activate(self):
        self.active = True
        self.current_length = 0
    
    def update(self, dt):
        if self.active and self.current_length < self.max_length:
            self.current_length += self.speed * dt
            if self.current_length > self.max_length:
                self.current_length = self.max_length
    
    def get_laser_positions(self, preview=False):
        if not self.active and not preview:
            return []

        positions = []
        pos = self.start_pos.copy()
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)

        length = int(self.max_length if preview else self.current_length)

        for _ in range(length):
            if 0 <= pos.x < map_w and 0 <= pos.y < map_h:
                positions.append(pos.copy())
                pos += self.direction
            else:
                break

        return positions
    
    
    def check_collision(self, body_list):
        if not self.active:
            return False
        
        laser_positions = self.get_laser_positions()
        for laser_pos in laser_positions:
            # Làm tròn vị trí laser về grid
            grid_x = int(laser_pos.x + 0.5)  # Làm tròn chuẩn
            grid_y = int(laser_pos.y + 0.5)
            grid_pos = Vector2(grid_x, grid_y)
            
            # Kiểm tra va chạm với từng phần thân rắn
            if grid_pos in body_list:
                return True
        return False
    
    def draw(self, surface, camera_offset=(0, 0)):
        if not self.active:
            return
        
        laser_positions = self.get_laser_positions()
        
        for i, pos in enumerate(laser_positions):
            x = pos.x * TILE_SIZE - camera_offset[0]
            y = pos.y * TILE_SIZE - camera_offset[1]
            
            # Phần tròn luôn ở cuối (đầu laser đang chạy)
            if i == len(laser_positions) - 1:
                surface.blit(self.laser_head, (x, y))
            else:
                surface.blit(self.laser_body, (x, y))