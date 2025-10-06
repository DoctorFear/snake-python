import pygame
from pygame.math import Vector2
from setting import *
from snake import Snake
from food import Food
from sprite import Sprite
from pytmx.util_pygame import load_pygame
from support import import_image

class Game:
    def __init__(self, groups, tmx_path='data/levels/222.tmx'):
        self.groups = groups
        self.tmx_map = load_pygame(tmx_path)
        # Cập nhật kích thước bản đồ
        global GAME_WIDTH, GAME_HEIGHT
        GAME_WIDTH = self.tmx_map.width * TILE_SIZE
        GAME_HEIGHT = self.tmx_map.height * TILE_SIZE
        # Load sound effect
        pygame.mixer.init()
        self.collect_sound = pygame.mixer.Sound("data/sounds/collect.wav")
        self.dead_sound = pygame.mixer.Sound("data/sounds/dead_1.wav")
        pygame.mixer.music.load("data/sounds/pixel-song.wav")
        # Chạy nhạc nền loop vô tận (-1 = loop infinite)
        pygame.mixer.music.play(-1)
        # Tùy chỉnh volume (0.0 ~ 1.0)
        pygame.mixer.music.set_volume(0.5)
        # Lấy danh sách vị trí hợp lệ cho thức ăn
        self.valid_positions = self.get_valid_positions()
        self.walls = []
        self.is_game_over = False

        self.background = import_image('graphics', 'backgrounds', 'forest', alpha=False)
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.setup()

    def setup(self):
        # Tạo tường trước để đảm bảo valid_positions chính xác
        self.walls = self.create_walls()
        # Load spawn point cho rắn từ Object Layer
        snake_spawn = None
        for obj in self.tmx_map.objects:
            if obj.name == 'spawn':
                snake_spawn = (obj.x, obj.y)
                break
        if snake_spawn is None:
            snake_spawn = (WIDTH // 2, HEIGHT // 2)  # Fallback
        self.snake = Snake(snake_spawn, self.groups, GAME_WIDTH, GAME_HEIGHT)
        self.food = Food(self.groups, self.snake, self.valid_positions)

    def get_valid_positions(self):
        valid_positions = []
        for y in range(self.tmx_map.height):
            for x in range(self.tmx_map.width):
                # Kiểm tra xem ô có phải là tường không
                is_wall = False
                for layer in self.tmx_map.visible_layers:
                    if hasattr(layer, 'tiles') and layer.name == 'Terrain':
                        if layer.data[y][x] != 0:  # Có tile tại vị trí (x, y)
                            is_wall = True
                            break
                if not is_wall:
                    valid_positions.append(Vector2(x, y))
        return valid_positions

    def create_walls(self):
        walls = []
        for layer in self.tmx_map.visible_layers:
            if hasattr(layer, 'tiles') and layer.name == 'Terrain':
                for x, y, surface in layer.tiles():
                    if surface:
                        pos = (x * TILE_SIZE, y * TILE_SIZE)
                        sprite = Sprite(pos, (TILE_SIZE, TILE_SIZE), (0, 0, 0), self.groups)
                        sprite.image = surface  # Sử dụng hình ảnh từ Tiled map
                        walls.append(Vector2(x, y))
        return walls

    def handle_input(self, key):
        if not self.is_game_over:
            self.snake.input(key)
        else:
            if key == pygame.K_SPACE:
                self.reset()

    def check_collisions(self):
        snake_head_pos = self.snake.body[0]
        food_grid_pos = Vector2(self.food.rect.x // TILE_SIZE, self.food.rect.y // TILE_SIZE)
        if snake_head_pos == food_grid_pos:
            self.snake.score += 1
            self.snake.grow()  # Gọi phương thức grow để tăng độ dài rắn
            self.collect_sound.play() #Sound effect khi ăn food
            self.food.respawn(self.snake)

    def reset(self):
        self.groups.empty()
        self.walls = self.create_walls()  # Tạo lại tường
        self.setup()  # Tạo lại rắn và thức ăn
        self.is_game_over = False

    def update(self, dt):
        if not self.is_game_over:
            self.is_game_over = self.snake.update(dt, self.food, self.walls, self.valid_positions)
            if self.is_game_over:
                self.dead_sound.play()  # Phát âm thanh khi chết
                pygame.mixer.music.stop() 
            self.check_collisions()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.groups.draw(self.snake)
        if self.is_game_over:
            font = pygame.font.SysFont('Arial', 50)
            text_surface = font.render('Game Over! Press Space', True, RED)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            surface.blit(text_surface, text_rect)