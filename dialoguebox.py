import pygame

class DialogueBox:
    def __init__(self, x, y, width, height, font=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font or pygame.font.Font(None, 28)
        self.text = ""
        self.timer = 0.0

    def set_text(self, text):
        self.text = text
        self.timer = 2.5  # seconds to display

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt
            if self.timer < 0:
                self.timer = 0

    def draw(self, surface):
        if self.timer > 0 and self.text:
            # Draw white box
            pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))
            # Draw black outline
            pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
            # Render and draw text (wrap if needed)
            text_surf = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(midleft=(self.x + 10, self.y + self.height // 2))
            surface.blit(text_surf, text_rect)
