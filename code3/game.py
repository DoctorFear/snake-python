import pygame
from pygame.math import Vector2
from setting import *
from snake import Snake
from food import Food
from sprite import Sprite
from enemy import Enemy
from pytmx.util_pygame import load_pygame
from support import import_image
from gui import render_text_with_shadow


class Game:
    def __init__(self, groups, tmx_path, mode, game_manager):
            self.groups = groups
            self.mode = mode 
            self.game_manager = game_manager
            self.tmx_map = load_pygame(tmx_path)
            global GAME_WIDTH, GAME_HEIGHT
            GAME_WIDTH = self.tmx_map.width * TILE_SIZE
            GAME_HEIGHT = self.tmx_map.height * TILE_SIZE
            pygame.mixer.init()
            self.collect_sound = pygame.mixer.Sound("data/sounds/collect.wav")
            self.dead_sound = pygame.mixer.Sound("data/sounds/dead_1.wav")
            self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
            # Apply volume
            self.collect_sound.set_volume(self.game_manager.sfx_volume / 100)
            self.dead_sound.set_volume(self.game_manager.sfx_volume / 100)
            self.click_sound.set_volume(self.game_manager.sfx_volume / 100)    

            self.music_file = "data/sounds/pixel-song.wav"
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.game_manager.music_volume / 100)

            self.valid_positions = self.get_valid_positions()
            self.walls = []
            
            background_file = 'forest3' if mode == 'easy' else 'forest4'
            self.background = import_image('graphics', 'backgrounds', background_file, alpha=False)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            self.setup()
            self.enemy = None
            self.enemy_spawn_time = None
            self.enemy_active = False

            # === Pause Menu ===
            self.is_paused = False
            self.menu_options = ["resume", "restart", "leave"]
            self.selected_index = 0  # Mặc định chọn resume

            # === Game Over Menu ===
            self.is_game_over = False
            self.over_menu_options = ["restart", "leave"]
            self.over_selected_index = 0 # Mặc định chọn restart


    def setup(self):
        self.walls = self.create_walls()
        snake_spawn = None
        for obj in self.tmx_map.objects:
            if obj.name == 'spawn':
                snake_spawn = (obj.x, obj.y)
                break
        if snake_spawn is None:
            snake_spawn = (WIDTH // 2, HEIGHT // 2)
        self.snake = Snake(snake_spawn, self.groups, GAME_WIDTH, GAME_HEIGHT, self.mode, self.game_manager, skin=self.game_manager.selected_skin)
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
        # === ƯU TIÊN KIỂM TRA GAME OVER MENU TRƯỚC ===
        if self.is_game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.over_selected_index = (self.over_selected_index - 1) % len(self.over_menu_options)
                    self.click_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.over_selected_index = (self.over_selected_index + 1) % len(self.over_menu_options)
                    self.click_sound.play()
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    selected = self.over_menu_options[self.over_selected_index]
                    if selected == "restart":
                        self.reset()
                        self.game_manager.apply_volume()
                    elif selected == "leave":
                        pygame.mixer.music.stop()
                        return "menu"
            return  # ⛔ Dừng luôn, không xử lý phần khác

        # === PAUSE MENU ===
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not self.is_game_over:
                self.is_paused = not self.is_paused
                if self.is_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                return

            if self.is_paused:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_options)
                    self.click_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_options)
                    self.click_sound.play()
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    selected = self.menu_options[self.selected_index]
                    if selected == "resume":
                        self.is_paused = False
                        pygame.mixer.music.unpause()
                    elif selected == "restart":
                        self.reset()
                        self.game_manager.apply_volume()
                        self.is_paused = False
                        pygame.mixer.music.unpause()
                    elif selected == "leave":
                        pygame.mixer.music.stop()
                        return "menu"
                return


            # === Điều khiển rắn bình thường ===
            self.snake.input(event)

        elif event.type == pygame.KEYUP and not self.is_paused:
            self.snake.input(event)


    def check_collisions(self):
        snake_head_pos = self.snake.body[0]
        food_grid_pos = Vector2(self.food.rect.x // TILE_SIZE, self.food.rect.y // TILE_SIZE)
        if snake_head_pos == food_grid_pos:
            self.snake.score += 1
            self.snake.grow()
            self.collect_sound.play()
            self.food.respawn(self.snake)

            if self.snake.score % 5 == 0:
                self.enemy = Enemy(self.groups, self.snake, self.valid_positions,
                                   self.tmx_map.width * TILE_SIZE,
                                   self.tmx_map.height * TILE_SIZE,
                                   self.mode)
                self.enemy_spawn_time = pygame.time.get_ticks()
                self.enemy_active = True

    def reset(self):
        self.groups.empty()
        self.walls = self.create_walls()
        self.setup()
        self.is_game_over = False
        self.enemy = None
        self.enemy_active = False
        self.enemy_spawn_time = None
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def update(self, dt):
        if self.is_paused or self.is_game_over:
            return

        self.food.update(dt)
        self.is_game_over = self.snake.update(dt, self.food, self.walls)
        
        if self.is_game_over:
            self.dead_sound.play()
            pygame.mixer.music.stop()

        self.check_collisions()

        if self.enemy:
            self.enemy.update(dt)
            if self.enemy.check_collision_with_snake(self.snake):
                self.is_game_over = True
                self.dead_sound.play()
                pygame.mixer.music.stop()
            
            elapsed = (pygame.time.get_ticks() - self.enemy_spawn_time) / 1000
            if elapsed >= 6:
                self.enemy.kill()
                self.enemy = None
                self.enemy_active = False
                self.enemy_spawn_time = None

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        # Vẽ walls (vật cản)
        for sprite in self.groups:
            if hasattr(sprite, 'image') and sprite not in [self.snake, self.food, self.enemy]:
                surface.blit(sprite.image, sprite.rect)
                
        self.snake.draw(surface)
        surface.blit(self.food.image, self.food.rect)

        if self.enemy:
            self.enemy.draw_laser(surface)
            surface.blit(self.enemy.image, self.enemy.rect)
            self.enemy.draw_warning(surface)

        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 20)
        score_text = render_text_with_shadow(
            f'Score: {self.snake.score}', font, WHITE, BLACK, shadow_offset=(2, 2)
        )
        surface.blit(score_text, (20, 0))

        if self.snake.show_unlock_message:
            unlock_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
            unlock_text = render_text_with_shadow(
                'Speed Boost Unlocked! Press S',
                unlock_font, WHITE, BLACK, shadow_offset=(2, 2)
            )
            unlock_rect = unlock_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            surface.blit(unlock_text, unlock_rect)

        if self.is_paused:
            self.draw_pause_menu(surface)

        if self.is_game_over:
            self.draw_game_over_menu(surface)


    # Hàm vẽ menu pause
    def draw_pause_menu(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Font
        try:
            title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 60)
            btn_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 40)
        except Exception as e:
            print("Warning: load font failed:", e)
            title_font = pygame.font.SysFont("Arial", 60)
            btn_font = pygame.font.SysFont("Arial", 40)

        # Title
        title = title_font.render('GAME PAUSED', True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120)))

        # Vẽ từng lựa chọn trong menu
        for i, name in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_index else (180, 180, 180)
            text = btn_font.render(name.capitalize(), True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
            surface.blit(text, text_rect)

            # Vẽ mũi tên trắng bên trái cho mục được chọn
            if i == self.selected_index:
                size = 25
                arrow_y = text_rect.centery + 6
                arrow_x = WIDTH // 2 - 150
                pygame.draw.polygon(surface, (255, 255, 255), [
                    (arrow_x, arrow_y),
                    (arrow_x - size, arrow_y - size * 0.7),
                    (arrow_x - size, arrow_y + size * 0.7)
                ])


    def draw_game_over_menu(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        try:
            title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 60)
            btn_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 40)
        except Exception:
            title_font = pygame.font.SysFont("Arial", 60)
            btn_font = pygame.font.SysFont("Arial", 40)

        # Tiêu đề
        title = title_font.render("GAME OVER", True, (255, 60, 60))
        surface.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120)))

        # Vẽ nút menu
        for i, name in enumerate(self.over_menu_options):
            color = WHITE if i == self.over_selected_index else (150, 150, 150)
            text = btn_font.render(name.capitalize(), True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
            surface.blit(text, text_rect)

            # Mũi tên trắng bên trái
            if i == self.over_selected_index:
                size = 25
                arrow_y = text_rect.centery + 6
                arrow_x = WIDTH // 2 - 150
                pygame.draw.polygon(surface, WHITE, [
                    (arrow_x, arrow_y),
                    (arrow_x - size, arrow_y - size * 0.7),
                    (arrow_x - size, arrow_y + size * 0.7)
                ])
