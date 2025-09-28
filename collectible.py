import pygame
import math

# Constants
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

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12
        self.color = YELLOW
        self.collected = False
        self.bob_timer = 0

        original_image = pygame.image.load("redbull.png").convert_alpha()
        width = int(original_image.get_width() * 0.1)
        height = int(original_image.get_height() * 0.1)
        self.image = pygame.transform.smoothscale(original_image, (width, height))
        
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        # Bobbing animation
        self.bob_timer += dt * 3
        if not self.collected:
            bob_offset = math.sin(self.bob_timer) * 5
            self.rect.centery = self.y + bob_offset

    def draw(self, screen):
        #if not self.collected:
        screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect