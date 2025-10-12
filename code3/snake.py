import pygame
from pygame.math import Vector2
from setting import TILE_SIZE
from support import import_image

class Snake(pygame.sprite.Sprite):
    def __init__(self, pos, groups, game_width, game_height):
        super().__init__(groups)
        self.game_width = game_width
        self.game_height = game_height

        # --- Load ảnh đầu (4 frame) ---
        self.head_images = [
            import_image('data', 'images', 'head', f'head_{i+1}', alpha=True)
            for i in range(4)
        ]
        self.current_head_frame = 0
        self.head_image = pygame.transform.scale(self.head_images[0], (TILE_SIZE, TILE_SIZE))

        # --- Load ảnh đuôi (4 frame) ---
        self.tail_images = [
            import_image('data', 'images', 'tail', f'tail_{i+1}', alpha=True)
            for i in range(4)
        ]
        self.current_tail_frame = 0
        self.tail_image = pygame.transform.scale(self.tail_images[0], (TILE_SIZE, TILE_SIZE))

        # --- Load ảnh thân (4 frame) ---
        self.body_images = [
            import_image('data', 'images', 'body', f'body_{i+1}', alpha=True)
            for i in range(4)
        ]
        self.current_body_frame = 0
        self.body_image = pygame.transform.scale(self.body_images[0], (TILE_SIZE, TILE_SIZE))

        self.move_sound = pygame.mixer.Sound("data/sounds/tap.wav")
        self.move_sound.set_volume(0.3)

        # --- Load ảnh góc ---
        self.corner_images = {}
        corner_configs = [
            ('right_to_up', '1a'),
            ('up_to_right', '2a'),
            ('up_to_left', '3a'),
            ('left_to_up', '4a'),
            ('left_to_down', '5a'),
            ('down_to_left', '6a'),
            ('down_to_right', '7a'),
            ('right_to_down', '8a')
        ]
        for name, file_name in corner_configs:
            self.corner_images[name] = pygame.transform.scale(
                import_image('data', 'images', 'rotate_body', file_name, alpha=True),
                (TILE_SIZE, TILE_SIZE)
            )

        # --- Khởi tạo ---
        self.image = self.head_image
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = Vector2(1, 0)
        self.body = [
            Vector2(pos[0] // TILE_SIZE, pos[1] // TILE_SIZE),
            Vector2(pos[0] // TILE_SIZE - 1, pos[1] // TILE_SIZE),
            Vector2(pos[0] // TILE_SIZE - 2, pos[1] // TILE_SIZE)
        ]
        self.segment_types = ['head', 'body', 'tail']

        self.time_since_move = 0
        self.base_move_interval = 0.15
        self.speed_multiplier = 1.0
        self.move_interval = self.base_move_interval / self.speed_multiplier
        self.new_direction = self.direction
        self.score = 0 

        # --- Animation ---
        self.frame_timer = 0
        self.frame_rate = 4  # 4 FPS (mỗi 0.25 giây đổi frame)

    # ------------------ INPUT ------------------
    def input(self, event):
        if event.type == pygame.KEYDOWN:
            old_dir = self.new_direction
            if event.key == pygame.K_UP and self.direction.y != 1:
                self.new_direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and self.direction.y != -1:
                self.new_direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and self.direction.x != 1:
                self.new_direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction.x != -1:
                self.new_direction = Vector2(1, 0)
            elif event.key == pygame.K_s:
                self.speed_multiplier = 2.0
            if self.new_direction != old_dir:
                self.move_sound.stop()
                self.move_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.speed_multiplier = 1.0

    # ------------------ COLLISION ------------------
    def check_collision(self, walls):
        new_head = self.body[0] + self.direction
        if (new_head in walls or
            new_head.x < 0 or new_head.x >= self.game_width // TILE_SIZE or
            new_head.y < 0 or new_head.y >= self.game_height // TILE_SIZE):
            print("Game over: Hit wall or boundary")
            return True
        if new_head in self.body[1:]:
            print("Game over: Collided with self")
            return True
        return False

    # ------------------ UPDATE ------------------
    def update(self, dt, food, walls):
        # --- Cập nhật animation (đầu & đuôi) ---
        self.frame_timer += dt
        if self.frame_timer >= 1 / self.frame_rate:
            self.current_head_frame = (self.current_head_frame + 1) % 4
            self.current_tail_frame = (self.current_tail_frame + 1) % 4
            self.head_image = pygame.transform.scale(self.head_images[self.current_head_frame], (TILE_SIZE, TILE_SIZE))
            self.tail_image = pygame.transform.scale(self.tail_images[self.current_tail_frame], (TILE_SIZE, TILE_SIZE))
            self.frame_timer = 0

        # --- Cập nhật di chuyển ---
        self.time_since_move += dt
        self.move_interval = self.base_move_interval / self.speed_multiplier
        if self.time_since_move >= self.move_interval:
            old_direction = self.direction
            self.direction = self.new_direction

            if self.check_collision(walls):
                # Nếu chết → trả hướng lại như cũ để giữ visual
                self.direction = old_direction
                return True
            new_head = self.body[0] + self.direction
            self.body.insert(0, new_head)
            self.segment_types.insert(0, 'head')
            self.body.pop()
            self.segment_types.pop()
            self.segment_types[0] = 'head'
            if len(self.segment_types) >= 2:
                self.segment_types[-1] = 'tail'
                if len(self.segment_types) > 2:
                    self.segment_types[1:-1] = ['body'] * (len(self.segment_types) - 2)
            self.rect.topleft = (new_head.x * TILE_SIZE, new_head.y * TILE_SIZE)
            self.time_since_move = 0
        return False

    # ------------------ GROW ------------------
    def grow(self):
        tail_dir = self.body[-2] - self.body[-1] if len(self.body) >= 2 else Vector2(1, 0)
        self.body.append(self.body[-1] - tail_dir)
        self.segment_types.append('tail')
        if len(self.segment_types) >= 2:
            self.segment_types[-2] = 'body'

    # ------------------ DRAW ------------------
    def draw(self, surface):
        for i, segment in enumerate(self.body):
            # Xác định vị trí từng đoạn
            segment_rect = pygame.Rect(
                segment.x * TILE_SIZE, 
                segment.y * TILE_SIZE, 
                TILE_SIZE, 
                TILE_SIZE
            )

            # --- ĐẦU RẮN ---
            if self.segment_types[i] == 'head':
                image = self.head_image
                angle = self.get_rotation_angle(self.direction)
                rotated_image = pygame.transform.rotate(image, angle)

            # --- ĐUÔI RẮN ---
            elif self.segment_types[i] == 'tail' and len(self.body) > 1:
                image = self.tail_image
                tail_direction = (self.body[-2] - self.body[-1]).normalize()
                angle = self.get_rotation_angle(tail_direction)
                rotated_image = pygame.transform.rotate(image, angle)

            # --- THÂN RẮN ---
            elif self.segment_types[i] == 'body' and len(self.body) > 1 and 0 < i < len(self.body) - 1:
                prev_segment = self.body[i - 1]
                next_segment = self.body[i + 1]

                prev_dir = (segment - prev_segment).normalize()
                next_dir = (next_segment - segment).normalize()

                # Nếu hướng khác nhau → là góc cua
                if prev_dir.x * next_dir.x + prev_dir.y * next_dir.y == 0:
                    corner_key = self.get_corner_key(prev_dir, next_dir)
                    rotated_image = self.corner_images.get(corner_key, self.body_image)
                else:
                    # Đoạn thẳng
                    direction = next_dir
                    angle = self.get_rotation_angle(direction)
                    rotated_image = pygame.transform.rotate(self.body_image, angle)

            # --- TRƯỜNG HỢP DỰ PHÒNG ---
            else:
                rotated_image = self.body_image

            # Vẽ đoạn rắn
            rotated_rect = rotated_image.get_rect(center=segment_rect.center)
            surface.blit(rotated_image, rotated_rect)


    # ------------------ ROTATION HELPERS ------------------
    def get_rotation_angle(self, direction):
        if direction.length() == 0:
            return 0
        direction = direction.normalize()
        if abs(direction.x) > abs(direction.y):
            return 0 if direction.x > 0 else 180
        else:
            return -90 if direction.y > 0 else 90

    def get_corner_key(self, prev_dir, next_dir):
        if prev_dir == Vector2(1, 0) and next_dir == Vector2(0, -1): return 'right_to_up'
        if prev_dir == Vector2(0, -1) and next_dir == Vector2(1, 0): return 'up_to_right'
        if prev_dir == Vector2(0, -1) and next_dir == Vector2(-1, 0): return 'up_to_left'
        if prev_dir == Vector2(-1, 0) and next_dir == Vector2(0, -1): return 'left_to_up'
        if prev_dir == Vector2(-1, 0) and next_dir == Vector2(0, 1): return 'left_to_down'
        if prev_dir == Vector2(0, 1) and next_dir == Vector2(-1, 0): return 'down_to_left'
        if prev_dir == Vector2(0, 1) and next_dir == Vector2(1, 0): return 'down_to_right'
        if prev_dir == Vector2(1, 0) and next_dir == Vector2(0, 1): return 'right_to_down'
        return 'right_to_up'
