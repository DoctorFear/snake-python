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
        pygame.mixer.music.load("data/sounds/theme.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

        self.buttons = [
            Button(WIDTH//2 - 200, HEIGHT//2 - 5, 400, 70, "Play", "#4d4d4d", "#3a3a3a", font),
            Button(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 70, "Settings", "#4d4d4d", "#3a3a3a", font),
            Button(1300, 660, 150, 70, "Quit", "#4d4d4d", "#3a3a3a", font),
            Button(40, 660, 150, 70, "Help", "#4d4d4d", "#3a3a3a", font)
            #Button(WIDTH//2 - 200, HEIGHT//2 - 5, 400, 70, "Play", "#5e503f","#3d2f23", font),    
            #Button(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 70, "Settings", "#5e503f","#3d2f23", font), 
            #Button(1300, 630, 150, 70, "Quit", "#5e503f", "#3d2f23", font)
        ]



    
    def draw(self, screen):
        # --- Nền gradient ---
        top_color = (0, 174, 239)
        bottom_color = (0, 114, 188)
        draw_gradient_background(screen, top_color, bottom_color)
        #top_color = (255, 196, 140)   
        #bottom_color = (179, 89, 0)   
        #draw_gradient_background(screen, top_color, bottom_color)
        
        
        # --- Tiêu đề ---
        title_font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 80)
        title_text = render_text_with_shadow("DRAGON HUNTER", title_font, WHITE, BLACK, shadow_offset=(0, 5))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 270))
        
        # --- Vẽ các nút ---
        for b in self.buttons:
            b.draw(screen)

    def handle_event(self, event):
        self.click_sound = pygame.mixer.Sound("data/sounds/tap.wav")
        self.click_sound.set_volume(0.3)
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