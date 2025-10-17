import pygame
import sys
sys.path.append('./code3')
from setting import WIDTH, HEIGHT, FPS
from game_manager import GameManager

def main():
    # Khởi tạo pygame 
    pygame.init()
    pygame.mixer.init()  # Tạo sound effect

        # --- Thêm icon ---
    icon = pygame.image.load("data/images/icon.png")
    pygame.display.set_icon(icon)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dragon Hunter")
    clock = pygame.time.Clock()
    
    # Tạo game manager
    game_manager = GameManager(screen)
    
    # Vòng lặp chính
    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)
        
        game_manager.update(dt)
        game_manager.draw()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()