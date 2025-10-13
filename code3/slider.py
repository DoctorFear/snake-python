import pygame

class Slider:
    """Thanh kéo chỉnh âm lượng (0 - 100)"""
    def __init__(self, x, y, width, height=10, min_value=0, max_value=100, initial_value=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_value
        self.max = max_value
        self.value = initial_value
        self.dragging = False

    def handle_event(self, event):
        """Xử lý sự kiện chuột"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.dragging = True
            self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        """Cập nhật giá trị slider theo vị trí chuột"""
        rel_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        self.value = int((rel_x / self.rect.width) * (self.max - self.min) + self.min)

    def draw(self, screen):
        """Vẽ thanh trượt"""
        # Track nền
        track_rect = pygame.Rect(self.rect.x, self.rect.y - 3, self.rect.width, 16)
        pygame.draw.rect(screen, (100, 100, 100), track_rect, border_radius=8)

        # Track đã fill (màu xanh sáng)
        fill_width = int((self.value - self.min) / (self.max - self.min) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y - 3, fill_width, 16)
            pygame.draw.rect(screen, (0,200,255), fill_rect, border_radius=8)     # Cam:  255,200,130

        # Knob (nút tròn)
        knob_x = int(self.rect.x + (self.value - self.min) / (self.max - self.min) * self.rect.width)
        knob_y = self.rect.y + 5

        # Shadow cho knob
        pygame.draw.circle(screen, (50, 50, 50), (knob_x + 2, knob_y + 2), 14)
        # Knob chính
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, knob_y), 14)
        # Viền knob
        pygame.draw.circle(screen, (0, 150, 220), (knob_x, knob_y), 14, 3)