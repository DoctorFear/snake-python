# snake/slider.py
import pygame

class Slider:
    """Thanh kéo chỉnh âm lượng"""
    def __init__(self, x, y, width, min_value=0, max_value=100, initial_value=50):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min = min_value
        self.max = max_value
        self.value = initial_value
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        rel_x = mouse_x - self.rect.x
        rel_x = max(0, min(rel_x, self.rect.width))
        self.value = int((rel_x / self.rect.width) * (self.max - self.min) + self.min)

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        knob_x = int(self.rect.x + (self.value - self.min) / (self.max - self.min) * self.rect.width)
        pygame.draw.circle(screen, (0, 0, 255), (knob_x, self.rect.y + 5), 8)
