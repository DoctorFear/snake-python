import pygame
from button import Button
from setting import WIDTH, HEIGHT, WHITE, GREEN, BLACK
import os

class GameModeSelector:
    """Menu chọn chế độ chơi"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.SysFont("Arial", 40)
        self.buttons = [
            Button(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 60, "Easy", (0,255,0), (100,255,100), font),
            Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 60, "Hard", (255,100,0), (255,150,50), font),
            Button(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 60, "Back", (150,150,150), (200,200,200), font)
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

    def draw_border(self, screen):
        """Vẽ viền gạch vàng xung quanh khung menu"""
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
        # --- Nền đen giống game ---
        screen.fill(BLACK)
        
        # --- Vẽ viền gạch vàng ---
        self.draw_border(screen)
        
        # --- Tiêu đề ---
        title_font = pygame.font.SysFont("Arial", 50)
        title = title_font.render("Select Mode", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 180))
        
        # --- Vẽ các nút ---
        for b in self.buttons:
            b.draw(screen)

    def handle_event(self, event):
        for b in self.buttons:
            if b.is_clicked(event):
                if b.text == "Easy":
                    self.game_manager.selected_mode = "easy"
                    self.game_manager.change_state("game")
                elif b.text == "Hard":
                    self.game_manager.selected_mode = "hard"
                    self.game_manager.change_state("game")
                elif b.text == "Back":
                    self.game_manager.change_state("menu")