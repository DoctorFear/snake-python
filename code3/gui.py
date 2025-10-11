import pygame

def render_text_with_shadow(text, font, text_color, shadow_color, shadow_offset=(3, 3)):
    """Tạo text với bóng đổ"""
    # Render text chính và shadow
    base_surface = font.render(text, False, text_color)
    shadow_surface = font.render(text, False, shadow_color)
    
    # Tạo surface đủ lớn chứa cả text và shadow
    offset_x, offset_y = shadow_offset
    w = base_surface.get_width() + abs(offset_x)
    h = base_surface.get_height() + abs(offset_y)
    result = pygame.Surface((w, h), pygame.SRCALPHA)
    
    # Vẽ shadow trước (phía dưới)
    result.blit(shadow_surface, (offset_x, offset_y))
    
    # Vẽ text chính lên trên
    result.blit(base_surface, (0, 0))
    
    return result

def draw_gradient_background(screen, top_color, bottom_color):
    """
    Vẽ nền gradient từ trên xuống dưới
    
    Args:
        screen: pygame screen object
        top_color: màu trên (tuple RGB)
        bottom_color: màu dưới (tuple RGB)
    """
    height = screen.get_height()
    
    for y in range(height):
        # Tính tỉ lệ màu theo chiều cao
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        
        pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))