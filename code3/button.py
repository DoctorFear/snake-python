import pygame

class Button:
    """Nút bấm trong menu"""
    def __init__(self, x, y, width, height, text, color, hover_color, font, shadow_offset=(5, 5)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.shadow_offset = shadow_offset

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hovered else self.color

        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset[0]
        shadow_rect.y += self.shadow_offset[1]
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect)

        pygame.draw.rect(screen, color, self.rect)
        
        text_surface = self.font.render(self.text, False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_rect.y -= 10
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

