import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # pixels per second

        # Load and scale player sprite smaller
        img_temp = pygame.image.load("redbull.png").convert_alpha()
        scale_factor = 0.3  # reduce to 30% of original size
        width = int(img_temp.get_width() * scale_factor)
        height = int(img_temp.get_height() * scale_factor)
        self.image = pygame.transform.smoothscale(img_temp, (width, height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt, keys):
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed * dt

        # Move player with screen bounds checking
        self.x = max(self.rect.width//2, min(SCREEN_WIDTH - self.rect.width//2, self.x + dx))
        self.y = max(self.rect.height//2, min(SCREEN_HEIGHT - self.rect.height//2, self.y + dy))
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect
