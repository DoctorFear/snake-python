import pygame
from setting import WIDTH, HEIGHT

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self, snake=None):
        # Vẽ tĩnh, không có offset camera (phù hợp với Snake game)
        # Vẽ các sprite khác (như thức ăn, tường) trước, sau đó vẽ rắn để đầu rắn hiển thị trên cùng
        for sprite in self.sprites():
            if sprite != snake:  # Vẽ thức ăn, tường và các sprite khác trước
                self.display_surface.blit(sprite.image, sprite.rect.topleft)
        if snake:
            snake.draw(self.display_surface)  # Vẽ rắn sau cùng