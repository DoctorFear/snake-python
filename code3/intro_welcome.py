import pygame
from button import Button
from setting import WIDTH, HEIGHT, WHITE

class IntroWelcome:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font_title = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 60)
        self.font_text = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
        #self.bg_color_top = (255, 180, 90)
        #self.bg_color_bottom = (230, 130, 30)
        self.bg_color_top = (0, 174, 239)      
        self.bg_color_bottom = (0, 114, 188) 


        self.button_next = Button(
            WIDTH // 2 - 100, HEIGHT - 120, 200, 60,
            "Next",  "#4d4d4d", "#3a3a3a", pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 25)
        )

    def draw_gradient(self, screen):
        """Vẽ nền chuyển màu"""
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(self.bg_color_top[0] * (1 - ratio) + self.bg_color_bottom[0] * ratio)
            g = int(self.bg_color_top[1] * (1 - ratio) + self.bg_color_bottom[1] * ratio)
            b = int(self.bg_color_top[2] * (1 - ratio) + self.bg_color_bottom[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    def draw(self, screen):
        self.draw_gradient(screen)

        title = self.font_title.render("Chào mừng Chiến binh Rồng!", True, WHITE)
        text_lines = [
            "Sau những giờ học tập và làm việc căng thẳng,",
            "hãy để Dragon Hunter dẫn bạn vào một cuộc phiêu lưu săn bắt đầy màu sắc.",
            "Chỉ vài phút thư giãn, bạn sẽ tái tạo lại năng lượng mạnh mẽ",
            "cho những hoạt động sắp tới."
        ]

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        y_offset = 250
        for line in text_lines:
            text_surface = self.font_text.render(line, True, WHITE)
            screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_offset))
            y_offset += 60

        self.button_next.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if self.button_next.is_clicked(event):
            self.game_manager.change_state("intro_description") 

