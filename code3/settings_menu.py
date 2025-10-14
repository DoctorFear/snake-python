import pygame
from button import Button
from slider import Slider
from gui import *
from setting import WIDTH, HEIGHT, WHITE, BLACK
import os

class SettingsMenu:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 25)
        self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
        self.click_sound.set_volume(0.3)

        self.selected_skin = "green"

        # --- Skin boxes ---
        box_size = 150
        spacing = 40
        left_center = WIDTH // 4
        self.skin1_rect = pygame.Rect(left_center - box_size - spacing//2, HEIGHT//2 - 20, box_size, box_size)
        self.skin2_rect = pygame.Rect(left_center + spacing//2, HEIGHT//2 - 20, box_size, box_size)

        # --- Load ảnh skin (giữ trong suốt) ---
        self.green_skin = pygame.image.load("data/images/green_dragon.png").convert_alpha()
        self.red_skin = pygame.image.load("data/images/red_dragon.png").convert_alpha()
        self.green_skin = pygame.transform.scale(self.green_skin, (box_size, box_size))
        self.red_skin = pygame.transform.scale(self.red_skin, (box_size, box_size))

        # 💡 Bo góc ảnh trực tiếp
        for_skin = [self.green_skin, self.red_skin]
        for i in range(len(for_skin)):
            size = for_skin[i].get_size()
            mask = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, *size), border_radius=16)
            rounded = for_skin[i].copy()
            rounded.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
            for_skin[i] = rounded

        self.green_skin, self.red_skin = for_skin

        # --- Volume slider ---
        slider_width = 350
        self.slider = Slider(3*WIDTH//4 - slider_width//2, HEIGHT//2 + 80, slider_width,
                             initial_value=self.game_manager.volume)

        # --- Back button ---
        self.back_btn = Button(WIDTH//2 - 100, HEIGHT - 120, 200, 60, "Back", "#4d4d4d", "#3a3a3a", font)


    def draw(self, screen):
        # --- Nền gradient ---
        top_color = (0, 174, 239)
        bottom_color = (0, 114, 188)
        draw_gradient_background(screen, top_color, bottom_color)

        # --- Tiêu đề ---
        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 50)
        title1_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 35)
        label_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 25)

        title = render_text_with_shadow("Settings", title_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        skin_y = 200
        skin_title = render_text_with_shadow("Skin", title1_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(skin_title, (WIDTH//4 - skin_title.get_width()//2, skin_y))

        vol_title = render_text_with_shadow("Volume", title1_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(vol_title, (3*WIDTH//4 - vol_title.get_width()//2, skin_y))

        # --- Vẽ vạch ngăn ---
        pygame.draw.line(screen, WHITE, (WIDTH//2, skin_y + 50), (WIDTH//2, HEIGHT - 200), 5)

        # --- Hiển thị ảnh skin ---
        screen.blit(self.green_skin, self.skin1_rect)
        screen.blit(self.red_skin, self.skin2_rect)

        # --- Label ---
        green_label = render_text_with_shadow("GREEN", label_font, WHITE, BLACK, shadow_offset=(0, 3))
        red_label = render_text_with_shadow("RED", label_font, WHITE, BLACK, shadow_offset=(0, 3))
        screen.blit(green_label, (self.skin1_rect.centerx - green_label.get_width()//2, self.skin1_rect.bottom + 15))
        screen.blit(red_label, (self.skin2_rect.centerx - red_label.get_width()//2, self.skin2_rect.bottom + 15))

        # --- Viền cho skin được chọn ---
        if self.selected_skin == "green":
            pygame.draw.rect(screen, (0, 255, 0), self.skin1_rect, 6, border_radius=8)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.skin2_rect, 6, border_radius=8)

        # --- Volume ---
        vol_value_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 35)
        vol_text = render_text_with_shadow(f"{self.slider.value}%", vol_value_font, WHITE, BLACK, shadow_offset=(0, 4))
        screen.blit(vol_text, (3*WIDTH//4 - vol_text.get_width()//2, HEIGHT//2 - 50))

        self.slider.draw(screen)
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

        # Slider
        old_value = self.slider.value
        self.slider.handle_event(event)
        if self.slider.value != old_value:
            self.game_manager.volume = self.slider.value
            self.game_manager.apply_volume()

        # Nút Back
        if self.back_btn.is_clicked(event):
            self.click_sound.play()
            self.game_manager.change_state("menu")
