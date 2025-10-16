import pygame
import random
from setting import TILE_SIZE, GAME_WIDTH, GAME_HEIGHT
from pygame.math import Vector2
from laser import Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, snake, valid_positions, game_width, game_height, mode, game_manager):
        super().__init__(groups)
        
        self.mode = mode
        self.game_manager = game_manager
        image_file = 'data/images/enemies/enemy1.png' if mode == 'easy' else 'data/images/enemies/enemy2.png'
        self.spawn_sound = pygame.mixer.Sound("data/sounds/enemy.wav")
        self.spawn_sound.set_volume(self.game_manager.sfx_volume / 100)
        spritesheet = pygame.image.load(image_file).convert_alpha()
        
        # 4 frames xếp theo lưới 2 cột x 2 hàng
        self.original_frames = []
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
            self.original_frames.append(frame)
        
        # Frames hiện tại (có thể bị xoay nếu là enemy2)
        self.frames = self.original_frames.copy()
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.image = self.frames[0]

        self.rect = self.image.get_rect()
        self.snake = snake
        self.valid_positions = valid_positions
        self.game_width = game_width
        self.game_height = game_height
        
        self.laser = None
        self.spawn_time = pygame.time.get_ticks()
        self.laser_fired = False

        # Thêm dấu chấm than nhấp nháy
        self.warning_blink = 0
        self.warning_visible = True
        self.warning_blink_speed = 0.2

        # Cờ để đánh dấu spawn thất bại
        self.spawn_failed = False
        
        # Set vị trí ngoài màn hình ban đầu
        self.rect.topleft = (-1000, -1000)
        
        self.spawn_at_edge()
    
    def spawn_at_edge(self):
        """Spawn enemy ở viền gần đuôi snake"""
        tail_pos = self.snake.body[-1]
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)

        # Xác định hướng di chuyển của đuôi
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
                laser_direction = Vector2(-1, 0)  # Bắn sang trái
            else:
                spawn_pos = Vector2(0, tail_pos.y)
                laser_direction = Vector2(1, 0)  # Bắn sang phải
        else:
            if direction.y > 0:
                spawn_pos = Vector2(tail_pos.x, map_h - 1)
                laser_direction = Vector2(0, -1)  # Bắn lên trên
            else:
                spawn_pos = Vector2(tail_pos.x, 0)
                laser_direction = Vector2(0, 1)  # Bắn xuống dưới

        # Nếu vị trí không hợp lệ, chọn random từ viền
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
                # Xác định hướng laser dựa trên vị trí spawn
                if spawn_pos.x == 0:
                    laser_direction = Vector2(1, 0)
                elif spawn_pos.x == map_w - 1:
                    laser_direction = Vector2(-1, 0)
                elif spawn_pos.y == 0:
                    laser_direction = Vector2(0, 1)
                else:
                    laser_direction = Vector2(0, -1)

        # ✅ CẢ 2 ENEMY ĐỀU SPAWN VÀO TRONG MAP 1 TILE (KHÔNG ở RÌA)
        # Tính toán vị trí spawn dựa trên hướng laser
        if laser_direction.x == 1:  # Bắn sang phải → spawn ở x=1
            spawn_pos = Vector2(1, spawn_pos.y)
        elif laser_direction.x == -1:  # Bắn sang trái → spawn ở x=map_w-2
            spawn_pos = Vector2(map_w - 2, spawn_pos.y)
        elif laser_direction.y == 1:  # Bắn xuống → spawn ở y=1
            spawn_pos = Vector2(spawn_pos.x, 1)
        elif laser_direction.y == -1:  # Bắn lên → spawn ở y=map_h-2
            spawn_pos = Vector2(spawn_pos.x, map_h - 2)
        
        # ✅ KIỂM TRA NẾU TRÙNG VỚI ĐUÔI SNAKE THÌ BỎ QUA (NGAY TỪ ĐẦU)
        if spawn_pos in self.snake.body:
            self.spawn_failed = True
            self.kill()  # Xóa enemy này luôn
            return
        
        # Chỉ set vị trí khi đã chắc chắn không trùng
        self.grid_pos = spawn_pos
        self.rect.topleft = (spawn_pos.x * TILE_SIZE, spawn_pos.y * TILE_SIZE)
        
        # Xoay enemy2 (tàu ngầm) theo hướng spawn
        if self.mode == 'hard':
            self.rotate_submarine(spawn_pos, laser_direction)
        
        # Khởi tạo object Laser
        self.laser = Laser(self.grid_pos, laser_direction, self.game_width, self.game_height, speed=30)

        if not self.spawn_failed:
            self.spawn_sound.play()
    
    def rotate_submarine(self, spawn_pos, laser_direction):
        """Xoay tàu ngầm theo laser_direction sao cho khớp yêu cầu của bạn:
        - top  -> xoay 180
        - bottom -> giữ nguyên
        - left -> xoay 90 (quay phải)
        - right -> xoay -90 (quay trái)
        """
        angle = 0

        # laser_direction là pygame.math.Vector2
        if laser_direction == Vector2(0, 1):      # bắn xuống => spawn ở rìa trên
            angle = 180
        elif laser_direction == Vector2(0, -1):   # bắn lên => spawn ở rìa dưới
            angle = 0
        elif laser_direction == Vector2(1, 0):    # bắn sang phải => spawn ở rìa trái
            angle = -90
        elif laser_direction == Vector2(-1, 0):   # bắn sang trái => spawn ở rìa phải
            angle = 90

        rotated_frames = []
        for frame in self.original_frames:
            rotated = pygame.transform.rotate(frame, angle)
            rotated_frames.append(rotated)

        self.frames = rotated_frames
        self.image = self.frames[self.current_frame]

    
    def update(self, dt):
        """Kiểm tra sau 3 giây thì bắn laser"""
        # Nếu spawn thất bại thì không update gì cả
        if self.spawn_failed:
            return
            
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000

        # Cập nhật nhấp nháy dấu chấm than (chỉ trước khi bắn)
        if elapsed < 3:
            self.warning_blink += dt
            if self.warning_blink >= self.warning_blink_speed:
                self.warning_blink = 0
                self.warning_visible = not self.warning_visible

        if elapsed >= 3 and not self.laser_fired:
            # Kích hoạt laser
            self.laser.activate()
            self.laser_fired = True
        
        # laser để nó bắn ra từ từ
        if self.laser:
            self.laser.update(dt)

        # Animation từ spritesheet
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw_laser(self, surface, camera_offset=(0, 0)):
        """Vẽ laser trên màn hình"""
        if self.laser and not self.spawn_failed:
            self.laser.draw(surface, camera_offset)
            
    def draw_warning(self, surface, camera_offset=(0, 0)):
        """Vẽ dấu chấm than cảnh báo phía trên enemy"""
        if self.spawn_failed:
            return
            
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000
        if elapsed < 3 and self.warning_visible:
            warning_x = self.rect.x - camera_offset[0] + TILE_SIZE // 2
            warning_y = self.rect.y - camera_offset[1] - 20
            
            font = pygame.font.Font(None, 60)
            warning_text = font.render("!", True, (255, 0, 0))
            warning_rect = warning_text.get_rect(center=(warning_x, warning_y))
            surface.blit(warning_text, warning_rect)

            # Vẽ đường laser cảnh báo (chớp đỏ)
            if self.laser:
                laser_positions = self.laser.get_laser_positions_preview()
                for pos in laser_positions:
                    x = pos.x * TILE_SIZE - camera_offset[0]
                    y = pos.y * TILE_SIZE - camera_offset[1]
                    
                    # Vẽ hình chữ nhật đỏ mờ
                    red_rect = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    red_rect.set_alpha(100)  # Độ mờ
                    red_rect.fill((255, 0, 0))
                    surface.blit(red_rect, (x, y))
    
    def check_collision_with_snake(self, snake):
        """Kiểm tra va chạm giữa snake với enemy hoặc laser"""
        if self.spawn_failed:
            return False
        
        # Va chạm với enemy
        for body_part in snake.body:
            if body_part == self.grid_pos:
                return True
        
        # Kiểm tra va chạm với laser
        if self.laser and self.laser.check_collision_with_body(snake.body):
            return True
        
        return False