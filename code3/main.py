import pygame
import sys
from setting import WIDTH, HEIGHT, FPS
from game import Game
from allsprites import AllSprites

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Nhóm sprite
all_sprites = AllSprites()
game = Game(all_sprites, 'data/levels/222.tmx')

# Main loop                                     
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game.handle_input(event.key)

    # Cập nhật
    game.update(dt)

    # Vẽ
    game.draw(screen)
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f"Score: {game.snake.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.quit()
sys.exit()