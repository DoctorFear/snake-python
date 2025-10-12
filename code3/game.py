import pygame
from pygame.math import Vector2
from setting import *
from snake import Snake
from food import Food
from sprite import Sprite
from pytmx.util_pygame import load_pygame
from support import import_image

class Game:
    def __init__(self, groups, tmx_path, mode):
        self.groups = groups
        self.tmx_map = load_pygame(tmx_path)
        global GAME_WIDTH, GAME_HEIGHT
        GAME_WIDTH = self.tmx_map.width * TILE_SIZE
        GAME_HEIGHT = self.tmx_map.height * TILE_SIZE
        pygame.mixer.init()
        self.collect_sound = pygame.mixer.Sound("data/sounds/collect.wav")
        self.dead_sound = pygame.mixer.Sound("data/sounds/dead_1.wav")
        pygame.mixer.music.load("data/sounds/hard-core.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)
        self.valid_positions = self.get_valid_positions()
        self.walls = []
        self.is_game_over = False
        background_file = 'forest3' if mode == 'easy' else 'forest4'
        self.background = import_image('graphics', 'backgrounds', background_file, alpha=False)
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.setup()

    def setup(self):
        self.walls = self.create_walls()
        snake_spawn = None
        for obj in self.tmx_map.objects:
            if obj.name == 'spawn':
                snake_spawn = (obj.x, obj.y)
                break
        if snake_spawn is None:
            snake_spawn = (WIDTH // 2, HEIGHT // 2)
        self.snake = Snake(snake_spawn, self.groups, GAME_WIDTH, GAME_HEIGHT)
        self.food = Food(self.groups, self.snake, self.valid_positions)

    def get_valid_positions(self):
        valid_positions = []
        for y in range(self.tmx_map.height):
            for x in range(self.tmx_map.width):
                is_wall = False
                for layer in self.tmx_map.visible_layers:
                    if hasattr(layer, 'tiles') and layer.name == 'Terrain':
                        if layer.data[y][x] != 0:
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
                        sprite.image = surface
                        walls.append(Vector2(x, y))
        return walls

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.is_game_over and event.key == pygame.K_SPACE:
                self.reset()
            else:
                self.snake.input(event)
        elif event.type == pygame.KEYUP:
            self.snake.input(event)

    def check_collisions(self):
        snake_head_pos = self.snake.body[0]
        food_grid_pos = Vector2(self.food.rect.x // TILE_SIZE, self.food.rect.y // TILE_SIZE)
        if snake_head_pos == food_grid_pos:
            self.snake.score += 1
            self.snake.grow()
            self.collect_sound.play()
            self.food.respawn(self.snake)

    def reset(self):
        self.groups.empty()
        self.walls = self.create_walls()
        self.setup()
        self.is_game_over = False
        pygame.mixer.music.play(-1)

    def update(self, dt):
        if not self.is_game_over:
            self.food.update() 
            self.is_game_over = self.snake.update(dt, self.food, self.walls)
            if self.is_game_over:
                self.dead_sound.play()
                self.dead_sound.set_volume(0.8)
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