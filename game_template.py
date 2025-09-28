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
        self.speed=200
        # Load sprite image
        img_temp = pygame.image.load("redbull.png").convert_alpha()
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

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.time_left=10
        self.high_score = 0

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r and self.state.game_over:
                    self.restart_game()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        for enemy in self.enemies:
            enemy.update(dt, self.player)
        for collectible in self.collectibles:
            collectible.update(dt)
        
        self.check_collisions()

        self.state.time_left -= dt
        if self.state.time_left <= 0:
            self.state.time_left = 0
            self.state.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects only if not over
        if not self.state.game_over:
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            for collectible in self.collectibles:
                collectible.draw(self.screen)
        
        # Draw UI on top
        self.draw_ui()
        
        # Draw game over overlay
        if self.state.game_over:
            if self.state.score > self.state.high_score:
                self.state.high_score = self.state.score
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)  # semi-transparent black
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            go_text = self.font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(go_text, go_rect)
            
            # Current score
            score_text = self.font.render(f"Score: {self.state.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(score_text, score_rect)
            
            # Highest score
            high_text = self.font.render(f"High Score: {self.state.high_score}", True, YELLOW)
            high_rect = high_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(high_text, high_rect)
            
            # Restart instructions
            restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def check_collisions(self):
        player_rect = self.player.get_rect()
        
        # Check enemy collisions
        for enemy in self.enemies[:]:
            if player_rect.colliderect(enemy.get_rect()):
                self.state.score -= 5  # <-- subtract 5 for hitting enemy
                print(f"Hit enemy! Score: {self.state.score}")
                self.enemies.remove(enemy)
        
        # Check collectible collisions
        for collectible in self.collectibles:
            if not collectible.collected and player_rect.colliderect(collectible.get_rect()):
                collectible.collected = True
                self.state.score += 10  # <-- add 10 for collectible
                print(f"Collected! Score: {self.state.score}")
            
    def draw_ui(self):
        # --- Score display ---
        score_text = self.font.render(f"Score: {self.state.score}", True, YELLOW)
        self.screen.blit(score_text, (10, 10))
        
        # --- Optional: show collectibles collected ---
        collected_count = sum(1 for c in self.collectibles if c.collected)
        total_collectibles = len(self.collectibles)
        coll_text = self.small_font.render(f"Collectibles: {collected_count}/{total_collectibles}", True, WHITE)
        self.screen.blit(coll_text, (10, 50))

        timer_text = self.font.render(f"Time Left: {int(self.state.time_left)}s", True, CYAN)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 250, 10))
        
    def reset_collectibles(self, index):
        for i in range(0,len(self.collectibles)):
            if i!=index:
                self.collectibles[i].collected=False

    def restart_game(self):
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.enemies = [Enemy(100, 100), Enemy(1100, 100)]
        for collectible in self.collectibles:
            collectible.collected = False
        self.state.game_over = False
        self.state.game_won = False
        self.state.score = 0
        self.state.time_left = 10

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
