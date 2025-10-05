import pygame
from pygame.math import Vector2

# Cấu hình màn hình
WIDTH = 1500                    
HEIGHT = 750
FPS = 60
TILE_SIZE = 50  # Kích thước ô nhỏ hơn để game mượt hơn

# Cấu hình bản đồ (sẽ được cập nhật từ file Tiled)
GAME_WIDTH = None
GAME_HEIGHT = None

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (150, 150, 150)
