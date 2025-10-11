import pygame
from button import Button
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
            Button(1250, 580, 150, 70, "Quit", "#4d4d4d", "#3a3a3a", font)
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

    def render_text_with_shadow(self, text, font, text_color, shadow_color, shadow_offset=(3, 3)):
        """Tạo text với bóng đổ"""
        # Render text chính và shadow
        base_surface = font.render(text, False, text_color)
        shadow_surface = font.render(text, False, shadow_color)
        
        # Tạo surface đủ lớn chứa cả text và shadow
        offset_x, offset_y = shadow_offset
        w = base_surface.get_width() + abs(offset_x)
        h = base_surface.get_height() + abs(offset_y)
        result = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Vẽ shadow trước (phía dưới)
        result.blit(shadow_surface, (offset_x, offset_y))
        
        # Vẽ text chính lên trên
        result.blit(base_surface, (0, 0))
        
        return result
    
    def draw(self, screen):
        # --- Nền đen giống game ---
        top_color = (0, 174, 239)
        bottom_color = (0, 114, 188)
        height = screen.get_height()

        for y in range(height):
            # Tính tỉ lệ màu theo chiều cao
            ratio = y / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)

            pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))
        
        # --- Vẽ viền gạch vàng ---
        self.draw_border(screen)
        
        # --- Tiêu đề ---
        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 80)
        title_text = self.render_text_with_shadow("Dragon Hunter", title_font, WHITE, BLACK, shadow_offset=(0, 5))
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