import pygame
from pygame.math import Vector2
from setting import TILE_SIZE

class Laser:
    """Class quản lý tia laser bắn từ enemy"""
    
    def __init__(self, start_pos, direction, game_width, game_height, speed=10):
        """
        Khởi tạo laser
        
        Args:
            start_pos (Vector2): Vị trí bắt đầu (grid coordinates)
            direction (Vector2): Hướng bắn laser
            game_width (int): Chiều rộng map (pixels)
            game_height (int): Chiều cao map (pixels)
            speed (int): Tốc độ bắn laser (tiles per second) - ✅ THÊM
        """
        self.start_pos = start_pos.copy()
        self.direction = direction.copy()
        self.game_width = game_width
        self.game_height = game_height
        self.active = False  # Laser có đang hoạt động không
        self.color = (255, 0, 0)  # Màu đỏ
        self.alpha = 150  # Độ trong suốt
        
        # ✅ THÊM: Thuộc tính cho hiệu ứng bắn từ từ
        self.speed = speed  # Tốc độ bắn (tiles/giây)
        self.current_length = 0  # Độ dài hiện tại của laser
        self.max_length = self._calculate_max_length()  # Độ dài tối đa
        self.is_fully_extended = False  # Đã bắn hết chưa
        
    def _calculate_max_length(self):
        """Tính độ dài tối đa của laser (số tiles đến khi ra khỏi map)"""
        current_pos = self.start_pos.copy()
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)
        
        length = 0
        while 0 <= current_pos.x < map_w and 0 <= current_pos.y < map_h:
            length += 1
            current_pos += self.direction
        
        return length
        
    def activate(self):
        """Kích hoạt laser"""
        self.active = True
        self.current_length = 0  # ✅ THÊM: Reset độ dài khi kích hoạt
        self.is_fully_extended = False
    
    def deactivate(self):
        """Tắt laser"""
        self.active = False
        self.current_length = 0  # ✅ THÊM: Reset độ dài
        self.is_fully_extended = False
    
    def update(self, dt):
        """
        ✅ THÊM MỚI: Cập nhật độ dài laser theo thời gian
        
        Args:
            dt (float): Delta time (giây)
        """
        if not self.active:
            return
        
        if not self.is_fully_extended:
            # Tăng độ dài laser theo tốc độ
            self.current_length += self.speed * dt
            
            # Giới hạn độ dài tối đa
            if self.current_length >= self.max_length:
                self.current_length = self.max_length
                self.is_fully_extended = True
    
    def get_laser_positions(self):
        """
        Tính toán tất cả vị trí grid mà laser đi qua
        
        Returns:
            list: Danh sách các Vector2 (grid positions)
        """
        if not self.active:
            return []
        
        laser_positions = []
        current_pos = self.start_pos.copy()
        map_w = int(self.game_width / TILE_SIZE)
        map_h = int(self.game_height / TILE_SIZE)
        
        # ✅ SỬA: Chỉ bắn đến current_length thay vì hết map
        tiles_drawn = 0
        while (0 <= current_pos.x < map_w and 0 <= current_pos.y < map_h 
               and tiles_drawn < int(self.current_length)):
            laser_positions.append(current_pos.copy())
            current_pos += self.direction
            tiles_drawn += 1
        
        return laser_positions
    
    def check_collision(self, position):
        """
        Kiểm tra 1 vị trí có va chạm với laser không
        
        Args:
            position (Vector2): Vị trí cần kiểm tra (grid coordinates)
            
        Returns:
            bool: True nếu va chạm
        """
        if not self.active:
            return False
        
        laser_positions = self.get_laser_positions()
        return position in laser_positions
    
    def check_collision_with_body(self, body_list):
        """
        Kiểm tra danh sách vị trí có va chạm với laser không
        
        Args:
            body_list (list): Danh sách các Vector2 positions
            
        Returns:
            bool: True nếu có bất kỳ phần nào va chạm
        """
        if not self.active:
            return False
        
        laser_positions = self.get_laser_positions()
        for body_part in body_list:
            if body_part in laser_positions:
                return True
        return False
    
    def draw(self, surface, camera_offset=(0, 0)):
        """
        Vẽ laser lên màn hình
        
        Args:
            surface: Pygame surface để vẽ
            camera_offset (tuple): Offset của camera (x, y)
        """
        if not self.active:
            return
        
        laser_positions = self.get_laser_positions()
        for pos in laser_positions:
            pixel_x = pos.x * TILE_SIZE - camera_offset[0]
            pixel_y = pos.y * TILE_SIZE - camera_offset[1]
            
            # Vẽ laser với độ trong suốt
            laser_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            laser_surface.fill(self.color)
            laser_surface.set_alpha(self.alpha)
            surface.blit(laser_surface, (pixel_x, pixel_y))
    
    def set_color(self, color):
        """Thay đổi màu laser"""
        self.color = color
    
    def set_alpha(self, alpha):
        """Thay đổi độ trong suốt"""
        self.alpha = alpha
    
    def set_speed(self, speed):
        """✅ THÊM: Thay đổi tốc độ bắn laser"""
        self.speed = speed