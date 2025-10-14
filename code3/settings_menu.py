import pygame
from button import Button
from slider import Slider
from gui import *
from setting import WIDTH, HEIGHT, WHITE, BLACK
import os

class SettingsMenu:
    """Menu cài đặt"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 25)
        self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
        self.click_sound.set_volume(0.3)

        # Selected skin (Green hoặc Red)
        self.selected_skin = "green"

        # --- Skin boxes ---
        box_size = 150
        spacing = 40
        left_center = WIDTH // 4
        self.skin1_rect = pygame.Rect(left_center - box_size - spacing//2, HEIGHT//2 - 20, box_size, box_size)
        self.skin2_rect = pygame.Rect(left_center + spacing//2, HEIGHT//2 - 20, box_size, box_size)

        # --- Volume slider ---
        slider_width = 350
        self.music_slider = Slider(3*WIDTH//4 - slider_width//2, HEIGHT//2 - 20, slider_width, initial_value=self.game_manager.music_volume)
        self.sfx_slider = Slider(3*WIDTH//4 - slider_width//2, HEIGHT//2 + 100, slider_width, initial_value=self.game_manager.sfx_volume)
        # --- Back button ---
        self.back_btn = Button(WIDTH//2 - 100, HEIGHT - 120, 200, 60, "Back", "#4d4d4d", "#3a3a3a", font)

    def draw(self, screen):
        top_color = (0, 174, 239)
        bottom_color = (0, 114, 188)
        draw_gradient_background(screen, top_color, bottom_color)

        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 50)
        title1_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 35)
        label_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 25)

        # === Title ===
        title = render_text_with_shadow("Settings", title_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        # === Bên trái: Skin ===
        skin_y = 200
        skin_title = render_text_with_shadow("Skin", title1_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(skin_title, (WIDTH//4 - skin_title.get_width()//2, skin_y))

        # === Bên phải: Volume (cao ngang Skin) ===
        vol_title = render_text_with_shadow("Volume", title1_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(vol_title, (3*WIDTH//4 - vol_title.get_width()//2, skin_y))

        # --- Vẽ vạch ngăn ---
        pygame.draw.line(screen, WHITE, (WIDTH//2, skin_y + 50), (WIDTH//2, HEIGHT - 200), 5)

        # === SKIN BOXES ===
        pygame.draw.rect(screen, WHITE, self.skin1_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.skin2_rect, border_radius=8)

        green_label = render_text_with_shadow("GREEN", label_font, WHITE, BLACK, shadow_offset=(0, 3))
        red_label = render_text_with_shadow("RED", label_font, WHITE, BLACK, shadow_offset=(0, 3))
        screen.blit(green_label, (self.skin1_rect.centerx - green_label.get_width()//2, self.skin1_rect.bottom + 15))
        screen.blit(red_label, (self.skin2_rect.centerx - red_label.get_width()//2, self.skin2_rect.bottom + 15))

        if self.selected_skin == "green":
            pygame.draw.rect(screen, (0, 255, 0), self.skin1_rect, 6, border_radius=8)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.skin2_rect, 6, border_radius=8)

        # === Volume sliders ===
        # Music label & slider
        music_label = render_text_with_shadow("Music", label_font, WHITE, BLACK, shadow_offset=(0, 3))
        music_label_y = skin_y + 110
        screen.blit(music_label, (3*WIDTH//4 - music_label.get_width()//2, music_label_y))
        self.music_slider.rect.y = music_label_y + 70 
        self.music_slider.draw(screen)

        # SFX label & slider
        sfx_label = render_text_with_shadow("SFX", label_font, WHITE, BLACK, shadow_offset=(0, 3))
        sfx_label_y = music_label_y + 120 
        screen.blit(sfx_label, (3*WIDTH//4 - sfx_label.get_width()//2, sfx_label_y))
        self.sfx_slider.rect.y = sfx_label_y + 70 
        self.sfx_slider.draw(screen)

        # === Back button ===
        self.back_btn.draw(screen)

    def handle_event(self, event):
        # Chọn skin
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.skin1_rect.collidepoint(event.pos):
                self.selected_skin = "green"
                self.click_sound.play()
            elif self.skin2_rect.collidepoint(event.pos):
                self.selected_skin = "red"
                self.click_sound.play()

        # Music slider
        old_music = self.music_slider.value
        self.music_slider.handle_event(event)
        if self.music_slider.value != old_music:
            self.game_manager.music_volume = self.music_slider.value
            pygame.mixer.music.set_volume(self.game_manager.music_volume / 100)

        # SFX slider
        old_sfx = self.sfx_slider.value
        self.sfx_slider.handle_event(event)
        if self.sfx_slider.value != old_sfx:
            self.game_manager.sfx_volume = self.sfx_slider.value
            self.click_sound.set_volume(self.game_manager.sfx_volume / 100)

        # Back button
        if self.back_btn.is_clicked(event):
            self.click_sound.play()
            self.game_manager.change_state("menu")
