import pygame
from pygame.math import Vector2
from setting import TILE_SIZE
from support import import_image

class Snake(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # Load images for head, body, tail

        self.head_image = import_image('data', 'images', 'head', alpha=True)
        self.body_image = import_image('data', 'images', 'body_straight', alpha=True)
        self.tail_image = import_image('data', 'images', 'tail', alpha=True)
        self.move_sound = pygame.mixer.Sound("data/sounds/tap.wav")

        # Load 8 corner images
        self.corner_images = {}
        corner_configs = [
            ('right_to_up', '1'),      # Phải -> Lên
            ('up_to_right', '2'),      # Lên -> Phải
            ('up_to_left', '3'),       # Lên -> Trái
            ('left_to_up', '4'),       # Trái -> Lên
            ('left_to_down', '5'),     # Trái -> Xuống
            ('down_to_left', '6'),     # Xuống -> Trái
            ('down_to_right', '7'),    # Xuống -> Phải
            ('right_to_down', '8')     # Phải -> Xuống
        ]
        
        for corner_name, file_name in corner_configs:
            self.corner_images[corner_name] = pygame.transform.scale(
                import_image('data', 'images', file_name, alpha=True), (TILE_SIZE, TILE_SIZE)
            )

        # Scale other images (head, body, tail)
        self.head_image = pygame.transform.scale(self.head_image, (TILE_SIZE, TILE_SIZE))
        self.body_image = pygame.transform.scale(self.body_image, (TILE_SIZE, TILE_SIZE))
        self.tail_image = pygame.transform.scale(self.tail_image, (TILE_SIZE, TILE_SIZE))

        # Set initial image (head)
        self.image = self.head_image
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = Vector2(1, 0)  # Hướng ban đầu: sang phải
        self.speed = 200
        self.body = [
            Vector2(pos[0] // TILE_SIZE, pos[1] // TILE_SIZE),  # Đầu
            Vector2(pos[0] // TILE_SIZE - 1, pos[1] // TILE_SIZE),  # Thân
            Vector2(pos[0] // TILE_SIZE - 2, pos[1] // TILE_SIZE)   # Đuôi
        ]
        self.segment_types = ['head', 'body', 'tail']
        self.score = 0
        self.time_since_move = 0
        self.move_interval = 0.15
        self.new_direction = self.direction

    def input(self,key):
        if key == pygame.K_UP and self.direction.y != 1:
            self.new_direction = Vector2(0, -1)
            self.move_sound.play()
        elif key == pygame.K_DOWN and self.direction.y != -1:
            self.new_direction = Vector2(0, 1)
            self.move_sound.play()
        elif key == pygame.K_LEFT and self.direction.x != 1:
            self.new_direction = Vector2(-1, 0)
            self.move_sound.play()
        elif key == pygame.K_RIGHT and self.direction.x != -1:
            self.new_direction = Vector2(1, 0)
            self.move_sound.play()

    def check_collision(self, walls):
        new_head = self.body[0] + self.direction
        if new_head in walls:
            return True
        if new_head in self.body[1:]:
            return True
        return False

    def grow(self):
        tail_dir = self.body[-2] - self.body[-1] if len(self.body) >= 2 else Vector2(1, 0)
        self.body.append(self.body[-1] - tail_dir)  # Thêm đoạn mới theo hướng đuôi
        self.segment_types.append('tail')
        if len(self.segment_types) >= 2:
            self.segment_types[-2] = 'body'


    def update(self, dt, food, walls):
        # self.input()
        self.time_since_move += dt
        if self.time_since_move >= self.move_interval:
            self.direction = self.new_direction
            new_head = self.body[0] + self.direction
            if self.check_collision(walls):
                return True
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

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            segment_rect = pygame.Rect(segment.x * TILE_SIZE, segment.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if self.segment_types[i] == 'head':
                image = self.head_image
                angle = self.get_rotation_angle(self.direction)
                rotated_image = pygame.transform.rotate(image, angle)
            elif self.segment_types[i] == 'tail' and len(self.body) > 1:
                image = self.tail_image
                tail_direction = self.body[-2] - self.body[-1]
                angle = self.get_rotation_angle(tail_direction)
                rotated_image = pygame.transform.rotate(image, angle)
            elif self.segment_types[i] == 'body' and len(self.body) > 1 and i > 0:
                prev_segment = self.body[i - 1]
                next_segment = self.body[i + 1] if i < len(self.body) - 1 else segment + self.direction
                prev_dir = segment - prev_segment
                next_dir = next_segment - segment
                if prev_dir.x * next_dir.x + prev_dir.y * next_dir.y == 0:  # Góc 90 độ
                    corner_key = self.get_corner_key(prev_dir, next_dir)
                    image = self.corner_images.get(corner_key, self.body_image)
                    rotated_image = image  # Không xoay, vì hình ảnh đã được thiết kế sẵn
                else:
                    image = self.body_image
                    direction = next_segment - prev_segment
                    angle = self.get_rotation_angle(direction)
                    rotated_image = pygame.transform.rotate(image, angle)
            else:
                rotated_image = self.body_image
            rotated_rect = rotated_image.get_rect(center=segment_rect.center)
            surface.blit(rotated_image, rotated_rect)

    def get_rotation_angle(self, direction):
        if direction.length() == 0:
            return 0
        direction = direction.normalize()
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                return 0
            else:
                return 180
        else:
            if direction.y > 0:
                return -90
            else:
                return 90
        return 0

    def get_corner_key(self, prev_dir, next_dir):
        """Xác định loại góc cua dựa trên hướng trước và sau"""
        if prev_dir == Vector2(1, 0) and next_dir == Vector2(0, -1):
            return 'right_to_up'      # Phải -> Lên
        elif prev_dir == Vector2(0, -1) and next_dir == Vector2(1, 0):
            return 'up_to_right'      # Lên -> Phải
        elif prev_dir == Vector2(0, -1) and next_dir == Vector2(-1, 0):
            return 'up_to_left'       # Lên -> Trái
        elif prev_dir == Vector2(-1, 0) and next_dir == Vector2(0, -1):
            return 'left_to_up'       # Trái -> Lên
        elif prev_dir == Vector2(-1, 0) and next_dir == Vector2(0, 1):
            return 'left_to_down'     # Trái -> Xuống
        elif prev_dir == Vector2(0, 1) and next_dir == Vector2(-1, 0):
            return 'down_to_left'     # Xuống -> Trái
        elif prev_dir == Vector2(0, 1) and next_dir == Vector2(1, 0):
            return 'down_to_right'    # Xuống -> Phải
        elif prev_dir == Vector2(1, 0) and next_dir == Vector2(0, 1):
            return 'right_to_down'    # Phải -> Xuống
        return 'right_to_up'  # Mặc định nếu không khớp

