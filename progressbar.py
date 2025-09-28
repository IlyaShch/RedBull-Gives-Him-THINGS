import pygame

class ProgressBar:
    def __init__(self, x, y, width, height, color, bg_color=(50, 50, 50), show_text=True, font=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = bg_color
        self.fullness = 1.0  # 0.0 (empty) to 1.0 (full)
        self.show_text = show_text
        self.font = font or pygame.font.Font(None, int(height * 0.8))

    def set_fullness(self, fullness):
        self.fullness = max(0.0, min(1.0, fullness))

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw foreground (fullness)
        fill_width = int(self.width * self.fullness)
        pygame.draw.rect(surface, self.color, (self.x, self.y, fill_width, self.height))
        # Draw percentage text
        if self.show_text:
            percent = int(self.fullness * 100)
            text = f"{percent}%"
            text_surf = self.font.render(text, True, (0,0,0) if self.fullness > 0.5 else (255,255,255))
            text_rect = text_surf.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            surface.blit(text_surf, text_rect)
