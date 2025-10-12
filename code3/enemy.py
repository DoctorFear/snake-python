import pygame
import random
from setting import TILE_SIZE, GAME_WIDTH, GAME_HEIGHT
from pygame.math import Vector2
from laser import Laser  # ✅ THÊM: Import class Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, snake, valid_positions, game_width, game_height):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((3, 53, 252))
        self.rect = self.image.get_rect()
        self.snake = snake
        self.valid_positions = valid_positions
        self.game_width = game_width
        self.game_height = game_height
        
        # ✅ SỬA: Thay vì các thuộc tính laser riêng lẻ, dùng object Laser
        self.laser = None  # Sẽ được khởi tạo sau khi spawn
        self.spawn_time = pygame.time.get_ticks()
        self.laser_fired = False
        
        self.spawn_at_edge_near_tail()
    
    def spawn_at_edge_near_tail(self):
        tail_pos = self.snake.body[-1]
        map_w, map_h = int(self.game_width / TILE_SIZE), int(self.game_height / TILE_SIZE)

        if len(self.snake.body) > 1:
            prev_tail = self.snake.body[-2]
            direction = tail_pos - prev_tail
        else:
            direction = Vector2(0, 1)

        # Chọn rìa tương ứng và xác định hướng laser
        laser_direction = Vector2(0, 0)
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                spawn_pos = Vector2(map_w - 1, tail_pos.y)
                offset = Vector2(-1, 0)
                laser_direction = Vector2(-1, 0)  # Bắn sang trái
            else:
                spawn_pos = Vector2(0, tail_pos.y)
                offset = Vector2(1, 0)
                laser_direction = Vector2(1, 0)  # Bắn sang phải
        else:
            if direction.y > 0:
                spawn_pos = Vector2(tail_pos.x, map_h - 1)
                offset = Vector2(0, -1)
                laser_direction = Vector2(0, -1)  # Bắn lên trên
            else:
                spawn_pos = Vector2(tail_pos.x, 0)
                offset = Vector2(0, 1)
                laser_direction = Vector2(0, 1)  # Bắn xuống dưới

        # Nếu vị trí không hợp lệ
        if spawn_pos not in self.valid_positions or spawn_pos in self.snake.body:
            edges = []
            for x in range(map_w):
                edges.append(Vector2(x, 0))
                edges.append(Vector2(x, map_h - 1))
            for y in range(map_h):
                edges.append(Vector2(0, y))
                edges.append(Vector2(map_w - 1, y))
            edges = [pos for pos in edges if pos in self.valid_positions and pos not in self.snake.body]
            if edges:
                spawn_pos = random.choice(edges)
                offset = Vector2(0, 0)
                # Xác định hướng laser dựa trên vị trí spawn
                if spawn_pos.x == 0:
                    laser_direction = Vector2(1, 0)
                elif spawn_pos.x == map_w - 1:
                    laser_direction = Vector2(-1, 0)
                elif spawn_pos.y == 0:
                    laser_direction = Vector2(0, 1)
                else:
                    laser_direction = Vector2(0, -1)

        # Xích vào trong 1 tile
        spawn_pos += offset
        self.grid_pos = spawn_pos
        self.rect.topleft = (spawn_pos.x * TILE_SIZE, spawn_pos.y * TILE_SIZE)
        
        #Khởi tạo object Laser
        self.laser = Laser(self.grid_pos, laser_direction, self.game_width, self.game_height, speed=30)
    
    def update(self, dt):
        """Kiểm tra sau 3 giây thì bắn laser"""
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000
        if elapsed >= 3 and not self.laser_fired:
            # Kích hoạt laser
            self.laser.activate()
            self.laser_fired = True
        
        #laser để nó bắn ra từ từ
        if self.laser:
            self.laser.update(dt)
    
    def draw_laser(self, surface, camera_offset=(0, 0)):
        """Vẽ laser trên màn hình"""
        if self.laser:
            self.laser.draw(surface, camera_offset)
    
    def check_collision_with_snake(self, snake):
        """Kiểm tra va chạm giữa snake với enemy hoặc laser"""
        
        # Va chạm với enemy
        for body_part in snake.body:
            if body_part == self.grid_pos:
                return True
        
        #Kiểm tra va chạm với laser
        if self.laser and self.laser.check_collision_with_body(snake.body):
            return True
        
        return False