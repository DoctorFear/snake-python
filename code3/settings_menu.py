import pygame
from button import Button
from slider import Slider
from setting import WIDTH, HEIGHT, WHITE, GREY, GREEN
import os

class SettingsMenu:
    """Menu cài đặt"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.SysFont("Arial", 35)

        self.speed = 0.5
        self.minus_btn = Button(WIDTH//2 - 120, 200, 50, 50, "-", GREY, (180,180,180), font)
        self.plus_btn = Button(WIDTH//2 + 70, 200, 50, 50, "+", GREY, (180,180,180), font)

        self.slider = Slider(WIDTH//2 - 150, 350, 300)
        self.back_btn = Button(WIDTH//2 - 100, 450, 200, 60, "Back", (150,150,150), (200,200,200), font)

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

    def draw_border(self, screen):
        """Vẽ viền vàng xung quanh khung menu"""
        if self.has_border:
            for x in range(0, WIDTH, self.tile_size):
                screen.blit(self.border_img, (x, 0))  # viền trên
                screen.blit(self.border_img, (x, HEIGHT - self.tile_size))  # viền dưới
            for y in range(0, HEIGHT, self.tile_size):
                screen.blit(self.border_img, (0, y))  # viền trái
                screen.blit(self.border_img, (WIDTH - self.tile_size, y))  # viền phải
        else:
            # Vẽ viền đơn giản nếu không có texture
            pygame.draw.rect(screen, (255, 215, 0), (0, 0, WIDTH, HEIGHT), 10)

    def draw(self, screen):
        # --- Nền đen để đồng bộ giao diện ---
        screen.fill((0, 0, 0))

        # --- Vẽ viền ---
        self.draw_border(screen)

        # --- Nội dung ---
        title_font = pygame.font.SysFont("Arial", 50)
        title = title_font.render("Settings", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        speed_font = pygame.font.SysFont("Arial", 30)
        speed_text = speed_font.render(f"Speed: {self.speed:.2f}", True, (255, 255, 255))
        screen.blit(speed_text, (WIDTH//2 - speed_text.get_width()//2, 160))

        self.minus_btn.draw(screen)
        self.plus_btn.draw(screen)
        self.slider.draw(screen)
        self.back_btn.draw(screen)

        vol_text = speed_font.render(f"Volume: {self.slider.value}%", True, (255, 255, 255))
        screen.blit(vol_text, (WIDTH//2 - vol_text.get_width()//2, 300))

    def handle_event(self, event):
        self.slider.handle_event(event)
        if self.minus_btn.is_clicked(event):
            self.speed = max(0.05, self.speed - 0.05)
        if self.plus_btn.is_clicked(event):
            self.speed = min(1.0, self.speed + 0.05)
        if self.back_btn.is_clicked(event):
            self.game_manager.change_state("menu")