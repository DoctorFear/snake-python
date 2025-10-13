import pygame
from menu import Menu
from game import Game
from settings_menu import SettingsMenu
from game_mode_selector import GameModeSelector
from allsprites import AllSprites
from intro_welcome import IntroWelcome
from intro_description import IntroDescription

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "intro_welcome"  # intro_welcome, intro_description, menu, mode_select, game, settings
        self.selected_mode = "easy"  # easy hoặc hard
        
        # --- Cài đặt game ---
        self.volume = 50  # Âm lượng (0 - 100)

        # --- Các thành phần ---
        self.all_sprites = AllSprites()
        self.intro_welcome = IntroWelcome(self)
        self.intro_description = IntroDescription(self)
        self.menu = Menu(self)
        self.settings_menu = SettingsMenu(self)
        self.mode_selector = GameModeSelector(self)
        self.game = None  # chỉ khởi tạo khi vào game

    def apply_volume(self):
        """Áp dụng âm lượng cho pygame mixer"""
        pygame.mixer.music.set_volume(self.volume / 100.0)
        # Áp dụng cho sound effects nếu game đang chạy
        if self.game:
            self.game.collect_sound.set_volume(self.volume / 100.0)
            self.game.dead_sound.set_volume(self.volume / 100.0)

    def change_state(self, new_state):
        """Chuyển trạng thái game"""
        if new_state == "game":
            self.all_sprites = AllSprites()
            # Chọn map dựa trên selected_mode
            map_path = 'data/levels/222 copy.tmx' if self.selected_mode == "easy" else 'data/levels/222.tmx'
            self.game = Game(self.all_sprites, map_path, mode=self.selected_mode, game_manager=self)
            # Áp dụng âm lượng cho game mới
            self.apply_volume()
        self.state = new_state

    def handle_event(self, event):
        """Xử lý sự kiện dựa trên trạng thái hiện tại"""
        if self.state == "intro_welcome":
            self.intro_welcome.handle_event(event)
        elif self.state == "intro_description":
            self.intro_description.handle_event(event)
        elif self.state == "menu":
            self.menu.handle_event(event)
        elif self.state == "mode_select":
            self.mode_selector.handle_event(event)
        elif self.state == "settings":
            self.settings_menu.handle_event(event)
        elif self.state == "game" and self.game:
            """Xử lý sự kiện trong game"""
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                result = self.game.handle_input(event)
                if result == "menu":
                    self.change_state("menu")

    def update(self, dt):
        """Cập nhật và quay về menu"""
        if self.state == "game" and self.game:
            self.game.update(dt)

    def draw(self):
        """Vẽ giao diện"""
        if self.state == "intro_welcome":
            self.intro_welcome.draw(self.screen)
        elif self.state == "intro_description":
            self.intro_description.draw(self.screen)
        elif self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "mode_select":
            self.mode_selector.draw(self.screen)
        elif self.state == "settings":
            self.settings_menu.draw(self.screen)
        elif self.state == "game" and self.game:
            self.game.draw(self.screen)
