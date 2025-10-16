import pygame
from button import Button
from setting import WIDTH, HEIGHT, WHITE, BLACK
from gui import *

class IntroDescription:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        # Font
        self.font_title = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 34)
        self.font_text = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 23)

        # Nút bắt đầu
        self.button_next = Button(
            WIDTH // 2 - 75, 660, 150, 70,
            "Back", "#4d4d4d", "#3a3a3a", pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
        )

    def draw(self, screen):
        # --- Nền chia đôi ---
        #left_color = (255, 180, 90)
        #right_color = (230, 130, 30)
        left_color = (0, 174, 239)
        right_color = (0, 114, 188)
        pygame.draw.rect(screen, left_color, (0, 0, WIDTH // 2, HEIGHT))
        pygame.draw.rect(screen, right_color, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

        # --- Nội dung CHẾ ĐỘ 1 ---
        lines1 = [
            "MODE 1: REBOOT",
            "",
            "You will play as Rosamo - the Young Dragon ", "on his journey to adulthood.", 
            "",
            "• Mission: Hunt for Sparkling Fish to gain ",
            "experience",
            "• Challenge: Every time Rosamo hunts 5",
            "Sparkling Fish, a Mysterious Machine will ",
            "activate, releasing a dangerous Aza Beam.",
            "• Once Rosamo has hunted 10 Sparkling Fish, ",
            "it will reach full maturity, gaining speed ",
            "boots for perfect dodging.",
            "• Suggest: Caution is key to getting through ",
            "this startup phase."
        ]

        # --- Nội dung CHẾ ĐỘ 2 ---
        lines2 = [
            "MODE 2: FINDING CHALLENGES",
            "",
            "You will play as Rosamo - Legendary Hunter",
            "willing to face the highest risks.",
            "",
            "• Mission: Hunting Sparkling Fish - Rosamo's ", 
            "source of energy.",
            "• Challenge: The danger level is doubled! For",
            "every 5 Sparkling Fish hunted, the Mysterious", 
            "Machine will fire a powerful Aza Beam.",
            "• Once Rosamo has hunted 10 Sparkling Fish, ",
            "it will reach full maturity, gaining speed ",
            "boots for perfect dodging.",
            "• Suggest: Be extremely alert! Obstacles have ",
            "been appearing all the time!"
        ]

        # --- Giãn dòng đều ---
        top_margin = 40
        line_gap_title = 35
        line_gap_text = 40

        # --- Cột trái ---
        y1 = top_margin
        for i, line in enumerate(lines1):
            font = self.font_title if i == 0 else self.font_text
            gap = line_gap_title if i == 0 else line_gap_text
            text_surface = render_text_with_shadow(line, font, WHITE, BLACK, shadow_offset=(0, 5))
            screen.blit(text_surface, (50, y1))
            y1 += gap

        # --- Cột phải ---
        y2 = top_margin
        for i, line in enumerate(lines2):
            font = self.font_title if i == 0 else self.font_text
            gap = line_gap_title if i == 0 else line_gap_text
            text_surface = render_text_with_shadow(line, font, WHITE, BLACK, shadow_offset=(0, 5))
            screen.blit(text_surface, (WIDTH // 2 + 50, y2))
            y2 += gap

        # --- Nút bắt đầu ---
        self.button_next.draw(screen)

    def handle_event(self, event):
        if self.button_next.is_clicked(event):
            self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
            self.click_sound.set_volume(self.game_manager.sfx_volume / 100)
            self.click_sound.play()
            self.game_manager.change_state("menu")
