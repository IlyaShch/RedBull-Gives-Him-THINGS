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

        original_image = pygame.image.load(r"C:\Users\jjand\Downloads\WTFareWeDOing\redbull.png").convert_alpha()
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
        if not self.collected:
            screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro 2d Topdown Game")
        self.clock = pygame.time.Clock()
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.enemies = [Enemy(100,100), Enemy(1100,100)]
        self.collectibles = [Collectible(400,300), Collectible(800,600)]
        self.running = True
        self.state = GameState()
        self.font = pygame.font.Font(None, 36)       # Big font for score
        self.small_font = pygame.font.Font(None, 24) # Smaller font for health

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
        
        self.check_collisions()

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for collectible in self.collectibles:
            collectible.draw(self.screen)
        
        self.draw_ui()

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)

        if self.state.game_over:
            self.screen.blit(overlay, (0,0))
            text = self.font.render("GAME OVER", True, RED)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, rect)
            score_text = self.font.render(f"Score: {self.state.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(score_text, score_rect)
        
        pygame.display.flip()
    
    def check_collisions(self):
        player_rect = self.player.get_rect()
        
        # Check enemy collisions
        for enemy in self.enemies[:]:  # Use slice to avoid modification during iteration
            if player_rect.colliderect(enemy.get_rect()):
                self.player.health -= 25
                if self.player.health <= 0:
                    self.state.game_over = True
                # Remove enemy after collision (or you could damage it instead)
                self.enemies.remove(enemy)
        
        # Check collectible collisions
        for collectible in self.collectibles:
            if not collectible.collected and player_rect.colliderect(collectible.get_rect()):
                collectible.collected = True
                self.state.score += 10
        
    def draw_ui(self):
        # --- Health bar ---
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = 10
        
        # Background (empty health)
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_width, health_height))
        
        # Current health
        current_health_width = int((self.player.health / self.player.max_health) * health_width)
        pygame.draw.rect(self.screen, GREEN, (health_x, health_y, current_health_width, health_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (health_x, health_y, health_width, health_height), 2)
        
        # Health text
        health_text = self.small_font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y + health_height + 5))
        
        # --- Collectibles/Score ---
        collected_count = sum(1 for c in self.collectibles if c.collected)
        total_collectibles = len(self.collectibles)
        score_text = self.font.render(f"Collectibles: {collected_count}/{total_collectibles}", True, YELLOW)
        self.screen.blit(score_text, (SCREEN_WIDTH - 250, 10))

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
