import pygame
from menu import Menu
from game import Game
from settings_menu import SettingsMenu
from game_mode_selector import GameModeSelector
from allsprites import AllSprites

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"  # menu, mode_select, game, settings
        self.selected_mode = "easy"  # easy hoặc hard
        
        # --- Cài đặt game ---
        self.volume = 50  # Âm lượng (0 - 100)

        # --- Các thành phần ---
        self.all_sprites = AllSprites()
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
        if new_state == "game":
            self.all_sprites = AllSprites()
            self.game = Game(self.all_sprites, 'data/levels/222 copy.tmx')
            # Áp dụng âm lượng cho game mới
            self.apply_volume()
        self.state = new_state

    def handle_event(self, event):
        if self.state == "menu":
            self.menu.handle_event(event)
        elif self.state == "mode_select":
            self.mode_selector.handle_event(event)
        elif self.state == "settings":
            self.settings_menu.handle_event(event)
        elif self.state == "game" and self.game:
            # Xử lý sự kiện cho game
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                result = self.game.handle_input(event)
                # Nếu game trả về "menu", chuyển về menu chính
                if result == "menu":
                    self.change_state("menu")

    def update(self, dt):
        if self.state == "game" and self.game:
            self.game.update(dt)

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "mode_select":
            self.mode_selector.draw(self.screen)
        elif self.state == "settings":
            self.settings_menu.draw(self.screen)
        elif self.state == "game" and self.game:
            self.game.draw(self.screen)