import pygame
from button import Button
from setting import WIDTH, HEIGHT, WHITE

class IntroDescription:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        # Font
        self.font_title = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 34)
        self.font_text = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 22)

        # Nút bắt đầu
        self.button_next = Button(
            WIDTH // 2 - 100, HEIGHT - 90, 200, 55,
            "Start", "#4d4d4d", "#3a3a3a", pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 25)
        )

    def draw(self, screen):
        # --- Nền chia đôi ---
        #left_color = (255, 180, 90)
        #right_color = (230, 130, 30)
        left_color = (0, 174, 239)
        right_color = (0, 114, 188)
        pygame.draw.rect(screen, left_color, (0, 0, WIDTH // 2, HEIGHT))
        pygame.draw.rect(screen, right_color, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

        # --- Nội dung CHẾ ĐỘ 1 ---
        lines1 = [
            "CHẾ ĐỘ 1: TÁI KHỞI ĐỘNG (DỄ)",
            "",
            "Bạn sẽ nhập vai Rosamo - Chú Rồng Trẻ đang ",
            "trên hành trình trưởng thành.", 
            "",
            "• Nhiệm vụ: Săn những Chú Cá Lấp Lánh để tích",
            "lũy kinh nghiệm.",
            "• Thử thách: Cứ mỗi khi Rosamo săn được 5 chú",
            "Cá Lấp Lánh, một Cổ Máy Bí Ẩn sẽ kích hoạt,",
            "phóng ra Chùm Sáng Aza nguy hiểm.",
            "• Khi săn đủ 10 chú Cá Lấp Lánh, Rosamo sẽ",
            "Trưởng Thành Toàn Diện, đạt được Tốc Độ ",
            "Bứt Phá để né tránh hoàn hảo.",
            "• Lưu ý: Sự cẩn trọng là chìa khóa để vượt ",
            "qua giai đoạn khởi động này."
        ]

        # --- Nội dung CHẾ ĐỘ 2 ---
        lines2 = [
            "CHẾ ĐỘ 2: TRUY TÌM THỬ THÁCH (KHÓ)",
            "",
            "Bạn sẽ nhập vai Rosamo - Thợ Săn Huyền Thoại",
            "đã sẵn sàng đối mặt với rủi ro cao nhất.",
            "",
            "• Nhiệm vụ: Vẫn là săn Chú Cá Lấp Lánh - nguồn ", 
            "năng lượng của Rosamo.",
            "• Thử thách: Mức độ nguy hiểm tăng gấp đôi!",
            "Cứ mỗi 8 chú Cá Lấp Lánh được săn, hai Cổ Máy", 
            "Bí Ẩn sẽ cùng khai hỏa Chùm Sáng Aza cực mạnh.",
            "• Khi săn đủ 8 chú Cá Lấp Lánh, Rosamo sẽ", 
            "Trưởng Thành Tức Thì, đạt được Tốc Độ Thần", 
            "Tốc để né tránh tối đa.",
            "• Cảnh báo: Hãy cực kỳ cảnh giác! Vật cản bất",
            "ngờ sẽ xuất hiện liên tục!"
        ]

        # --- Giãn dòng đều ---
        top_margin = 70
        line_gap_title = 40
        line_gap_text = 36

        # --- Cột trái ---
        y1 = top_margin
        for i, line in enumerate(lines1):
            color = WHITE
            font = self.font_title if i == 0 else self.font_text
            gap = line_gap_title if i == 0 else line_gap_text
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (50, y1))
            y1 += gap

        # --- Cột phải ---
        y2 = top_margin
        for i, line in enumerate(lines2):
            color = WHITE
            font = self.font_title if i == 0 else self.font_text
            gap = line_gap_title if i == 0 else line_gap_text
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (WIDTH // 2 + 50, y2))
            y2 += gap

        # --- Nút bắt đầu ---
        self.button_next.draw(screen)

    def handle_event(self, event):
        if self.button_next.is_clicked(event):
            self.game_manager.change_state("menu")
