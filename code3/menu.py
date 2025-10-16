import pygame
from button import Button
from gui import *
from setting import WIDTH, HEIGHT, WHITE, RED, BLUE, YELLOW, BLACK
import cv2

class Menu:
    """Menu chính"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 30)
        pygame.mixer.music.load("data/sounds/theme.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

        self.buttons = [
            Button(WIDTH//2 - 200, HEIGHT//2 - 5, 400, 70, "Play", "#4d4d4d", "#3a3a3a", font),
            Button(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 70, "Settings", "#4d4d4d", "#3a3a3a", font),
            Button(1300, 660, 150, 70, "Quit", "#4d4d4d", "#3a3a3a", font),
            Button(40, 660, 150, 70, "Help", "#4d4d4d", "#3a3a3a", font)
        ]

        # Mở video bằng OpenCV
        self.cap = cv2.VideoCapture("graphics/backgrounds/background.mp4")

    def draw(self, screen):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # === Giữ tỉ lệ và crop cho vừa màn hình ===
                vid_h, vid_w, _ = frame.shape
                scale = max(WIDTH / vid_w, HEIGHT / vid_h)  # phóng to vừa khít màn hình

                new_w, new_h = int(vid_w * scale), int(vid_h * scale)
                frame = cv2.resize(frame, (new_w, new_h))

                # Cắt giữa nếu kích thước vượt khung
                x_start = (new_w - WIDTH) // 2
                y_start = (new_h - HEIGHT) // 2
                frame = frame[y_start:y_start + HEIGHT, x_start:x_start + WIDTH]

                # Chuyển thành surface để vẽ
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                screen.blit(frame_surface, (0, 0))
        
        # --- Tiêu đề ---
        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 80)
        title_text = render_text_with_shadow("DRAGON HUNTER", title_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 270))
        
        # --- Vẽ các nút ---
        for b in self.buttons:
            b.draw(screen)

    def handle_event(self, event):
        self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
        self.click_sound.set_volume(self.game_manager.sfx_volume / 100)
        for b in self.buttons:
            if b.is_clicked(event):
                if b.text == "Play":
                    self.click_sound.play()
                    self.game_manager.change_state("mode_select")
                elif b.text == "Settings":
                    self.game_manager.change_state("settings")
                    self.click_sound.play()
                elif b.text == "Help":
                    self.game_manager.change_state("intro_welcome")
                    self.click_sound.play()  
                elif b.text == "Quit":
                    pygame.quit()
                    exit()
    
    def __del__(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()
