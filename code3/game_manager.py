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
        self.state = "menu"  # intro_welcome, intro_description, menu, mode_select, game, settings
        self.selected_mode = "easy"  # easy hoặc hard
        
        # --- Cài đặt game ---
        self.music_volume = 50  # 0-100
        self.sfx_volume = 50    # 0-100

        # --- Các thành phần ---
        self.all_sprites = AllSprites()
        self.intro_welcome = IntroWelcome(self)
        self.intro_description = IntroDescription(self)
        self.menu = Menu(self)
        self.settings_menu = SettingsMenu(self)
        self.mode_selector = GameModeSelector(self)
        self.game = None  # chỉ khởi tạo khi vào game

        self.selected_skin = "green" # Mặc định là skin xanh lá


    def apply_volume(self):
        """Áp dụng âm lượng cho pygame mixer"""
        pygame.mixer.music.set_volume(self.music_volume / 100.0)
        # Áp dụng cho sound effects nếu game đang chạy
        if self.game:
            self.game.collect_sound.set_volume(self.sfx_volume / 100.0)
            self.game.dead_sound.set_volume(self.sfx_volume / 100.0)
            # Điều chỉnh âm thanh tiếng click 
            if hasattr(self.game, "click_sound"):
                self.game.click_sound.set_volume(self.sfx_volume / 100.0)

    def change_state(self, new_state):
        """Chuyển trạng thái game mà không reset nhạc menu mỗi lần"""
        # Nếu vào game → dừng nhạc menu và khởi động game
        if new_state == "game":
            self.all_sprites = AllSprites()

            map_path = (
                'data/levels/222 copy.tmx'
                if self.selected_mode == "easy"
                else 'data/levels/222.tmx'
            )

            self.game = Game(self.all_sprites, map_path, mode=self.selected_mode, game_manager=self)
            self.apply_volume()

        else:
            # Nếu chuyển giữa các menu với nhau (menu, settings, mode select)
            # thì chỉ phát nhạc nếu nó chưa chạy
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("data/sounds/theme.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume / 100)
            else:
                # Nếu nhạc menu đang chạy rồi thì chỉ chỉnh lại volume cho đúng
                pygame.mixer.music.set_volume(self.music_volume / 100)

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
