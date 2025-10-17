import pygame
from button import Button
from setting import WIDTH, HEIGHT, WHITE, BLACK
from gui import *

class IntroWelcome:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font_title = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 60)
        self.font_text = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
        self.background_image = pygame.image.load("graphics/backgrounds/help_bg.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))


        self.button_next = Button(
            WIDTH // 2 - 75, 660, 150, 70,
            "Next",  "#4d4d4d", "#3a3a3a", pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
        )

    def draw(self, screen):
        """Chèn ảnh nền"""
        screen.blit(self.background_image, (0, 0))

        title = render_text_with_shadow("Welcome Dragon Warrior!", self.font_title, WHITE, BLACK, shadow_offset=(0, 5))
        text_lines = [
            "After stressful hours of studying and working,",
            "let Dragon Hunter lead you on a colorful hunting adventure.",
            "Just a few minutes of relaxation will recharge ",
            "your batteries for the activities ahead.",
            "",
            "Get ready to embark on an exciting journey with Rosamo!"
        ]

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))

        y_offset = 180
        for line in text_lines:
            text_surface = render_text_with_shadow(line, self.font_text, WHITE, BLACK, shadow_offset=(0, 5))
            screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_offset))
            y_offset += 60

        # --- Dòng hướng dẫn điều khiển (mũi tên có font riêng + đổ bóng đồng bộ) ---
        font_arrow = pygame.font.SysFont("segoeuisymbol", 35)
        parts = [
                ("←", font_arrow),
                (" : Move Left   ", self.font_text),
                ("→", font_arrow),
                (" : Move Right   ", self.font_text),
                ("↑", font_arrow),
                (" : Move Up   ", self.font_text),
                ("↓", font_arrow),
                (" : Move Down   S : Speed boots", self.font_text)
            ]

        # Tạo surface có hiệu ứng đổ bóng cho từng phần
        rendered_parts = []
        total_width = 0
        max_height = 0
        for text, font in parts:
            surf = render_text_with_shadow(text, font, WHITE, BLACK, shadow_offset=(0, 4))
            rendered_parts.append(surf)
            total_width += surf.get_width()
            max_height = max(max_height, surf.get_height())

        # Căn giữa toàn dòng
        start_x = WIDTH // 2 - total_width // 2
        y = HEIGHT - 210  # vị trí dọc tham chiếu (căn giữa dòng trên nút Next)

        # Vẽ từng phần, căn chỉnh theo chiều cao (vertical center) để tránh lệch
        x = start_x
        for surf in rendered_parts:
            offset_y = (max_height - surf.get_height()) // 2
            screen.blit(surf, (x, y + offset_y))
            x += surf.get_width()

        self.button_next.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if self.button_next.is_clicked(event):
            self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
            self.click_sound.set_volume(self.game_manager.sfx_volume / 100)
            self.click_sound.play()
            self.game_manager.change_state("intro_description") 

