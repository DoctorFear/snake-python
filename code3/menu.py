import pygame
from button import Button
from gui import *
from setting import WIDTH, HEIGHT, WHITE, RED, BLUE, YELLOW, BLACK
import os

class Menu:
    """Menu chính"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)

        self.buttons = [
            Button(WIDTH//2 - 200, HEIGHT//2 - 5, 400, 70, "Play", "#4d4d4d", "#3a3a3a", font),
            Button(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 70, "Settings", "#4d4d4d", "#3a3a3a", font),
            Button(1300, 630, 150, 70, "Quit", "#4d4d4d", "#3a3a3a", font)
        ]

        # --- Load texture viền ---
        border_path = os.path.join("graphics", "objects", "items", "sandstone_carved.png")
        try:
            self.border_img = pygame.image.load(border_path).convert_alpha()
            self.tile_size = self.border_img.get_width()
            self.has_border = True
        except Exception as e:
            print(f"Không thể load texture viền: {e}")
            # Nếu không tìm thấy texture, vẽ viền đơn giản
            self.has_border = False
            self.tile_size = 50

    # def draw_border(self, screen):
        # """Vẽ viền gạch vàng xung quanh khung menu"""
        # if self.has_border:
        #     for x in range(0, WIDTH, self.tile_size):
        #         screen.blit(self.border_img, (x, 0))  # viền trên
        #         screen.blit(self.border_img, (x, HEIGHT - self.tile_size))  # viền dưới
        #     for y in range(0, HEIGHT, self.tile_size):
        #         screen.blit(self.border_img, (0, y))  # viền trái
        #         screen.blit(self.border_img, (WIDTH - self.tile_size, y))  # viền phải
        # else:
        #     # Vẽ viền đơn giản nếu không có texture
        #     pygame.draw.rect(screen, (255, 215, 0), (0, 0, WIDTH, HEIGHT), 10)
    
    def draw(self, screen):
        # --- Nền gradient ---
        top_color = (0, 174, 239)
        bottom_color = (0, 114, 188)
        draw_gradient_background(screen, top_color, bottom_color)
        
        # --- Vẽ viền gạch vàng ---
        # self.draw_border(screen)
        
        # --- Tiêu đề ---
        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 80)
        title_text = render_text_with_shadow("DRAGON HUNTER", title_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 270))
        
        # --- Vẽ các nút ---
        for b in self.buttons:
            b.draw(screen)

    def handle_event(self, event):
        for b in self.buttons:
            if b.is_clicked(event):
                if b.text == "Play":
                    self.game_manager.change_state("mode_select")
                elif b.text == "Settings":
                    self.game_manager.change_state("settings")
                elif b.text == "Quit":
                    pygame.quit()
                    exit()