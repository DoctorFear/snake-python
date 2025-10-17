import pygame
from button import Button
from gui import *
from setting import WIDTH, HEIGHT, WHITE, GREEN, BLACK
import os

class GameModeSelector:
    """Menu chọn chế độ chơi"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
        self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
        self.buttons = [
            Button(WIDTH//2 - 100, HEIGHT//2 - 40, 220, 60, "Easy", "#4d4d4d", "#3a3a3a", font),
            Button(WIDTH//2 - 100, HEIGHT//2 + 40, 220, 60, "Hard", "#4d4d4d", "#3a3a3a", font),
            Button(40, 660, 150, 70, "Back", "#4d4d4d", "#3a3a3a", font)
        ]

    def draw(self, screen):
        # --- Chèn ảnh nền ---
        self.background_image = pygame.image.load("graphics/backgrounds/help_bg.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        screen.blit(self.background_image, (0, 0))
        
        
        # --- Tiêu đề ---
        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 50)
        title = render_text_with_shadow("Select Mode", title_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 200))
        
        # --- Vẽ các nút ---
        for b in self.buttons:
            b.draw(screen)

    def handle_event(self, event):
        self.click_sound.set_volume(self.game_manager.sfx_volume / 100)
        for b in self.buttons:
            if b.is_clicked(event):
                if b.text == "Easy":
                    self.click_sound.play()
                    self.game_manager.selected_mode = "easy"
                    self.game_manager.change_state("game")
                elif b.text == "Hard":
                    self.click_sound.play()
                    self.game_manager.selected_mode = "hard"
                    self.game_manager.change_state("game")
                elif b.text == "Back":
                    self.click_sound.play()
                    self.game_manager.change_state("menu")