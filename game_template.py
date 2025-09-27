import pygame
import sys
import math

# Initialize Pygame
pygame.init()

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

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # pixels per second
        self.health = 100
        self.max_health = 100

        # Load sprite image
        img_temp = pygame.image.load(r"C:\Users\jjand\Downloads\WTFareWeDOing\redbull.png").convert_alpha()
        width = int(img_temp.get_width() * 0.5)
        height = int(img_temp.get_height() * 0.5)
        self.image=pygame.transform.smoothscale(img_temp, (width, height))
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

        # Apply movement with screen bounds checking
        self.x = max(self.rect.width//2, min(SCREEN_WIDTH - self.rect.width//2, self.x + dx))
        self.y = max(self.rect.height//2, min(SCREEN_HEIGHT - self.rect.height//2, self.y + dy))

        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

# Minimal Enemy class for demo
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.speed = 50
        self.color = RED

    def update(self, dt, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x-8, self.y-8, 16, 16))

    def get_rect(self):
        return pygame.Rect(self.x-8, self.y-8, 16, 16)

# Simple Collectible class
class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12
        self.color = YELLOW
        self.collected = False
        self.bob_timer = 0

    def update(self, dt):
        self.bob_timer += dt * 3

    def draw(self, screen):
        if not self.collected:
            bob_offset = math.sin(self.bob_timer) * 3
            y_pos = self.y + bob_offset
            points = [
                (self.x, y_pos - self.size//2),
                (self.x + self.size//2, y_pos),
                (self.x, y_pos + self.size//2),
                (self.x - self.size//2, y_pos)
            ]
            pygame.draw.polygon(screen, self.color, points)

    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sprite Player Demo")
        self.clock = pygame.time.Clock()
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.enemies = [Enemy(100,100), Enemy(1100,100)]
        self.collectibles = [Collectible(400,300), Collectible(800,600)]
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        for enemy in self.enemies:
            enemy.update(dt, self.player)
        for collectible in self.collectibles:
            collectible.update(dt)

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for collectible in self.collectibles:
            collectible.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
