import math
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60

# Colors (retro palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


class Enemy:
    def __init__(self, x, y, image_path=None, scale=1.0, dialogue=""):
        self.x = x
        self.y = y
        self.size = 16
        self.speed = 50
        self.color = RED
        self.image = None
        self.rect = None
        self.dialogue = dialogue  # String field for enemy dialogue or label
        if image_path:
            img_temp = pygame.image.load(image_path).convert_alpha()
            width = int(img_temp.get_width() * scale)
            height = int(img_temp.get_height() * scale)
            self.image = pygame.transform.smoothscale(img_temp, (width, height))
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt
        if self.image:
            self.rect.center = (self.x, self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, (self.x-8, self.y-8, 16, 16))

    def get_rect(self):
        if self.image:
            return self.rect
        return pygame.Rect(self.x-8, self.y-8, 16, 16)