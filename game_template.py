import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (retro palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 200  # pixels per second
        self.color = CYAN
        self.health = 100
        self.max_health = 100
        
    def update(self, dt, keys):
        # Movement
        dx = 0
        dy = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed * dt
        
        # Apply movement with screen bounds checking
        self.x = max(self.size//2, min(SCREEN_WIDTH - self.size//2, self.x + dx))
        self.y = max(self.size//2, min(SCREEN_HEIGHT - self.size//2, self.y + dy))
    
    def draw(self, screen):
        # Draw player as a square
        rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        
        # Draw a simple direction indicator
        center = (self.x, self.y)
        pygame.draw.circle(screen, WHITE, center, 3)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.speed = 50
        self.color = RED
        self.health = 50
        
    def update(self, dt, player):
        # Simple AI: move towards player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and apply speed
            dx = (dx / distance) * self.speed * dt
            dy = (dy / distance) * self.speed * dt
            self.x += dx
            self.y += dy
    
    def draw(self, screen):
        rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 12
        self.color = YELLOW
        self.collected = False
        self.bob_timer = 0
        
    def update(self, dt):
        # Simple bobbing animation
        self.bob_timer += dt * 3
        
    def draw(self, screen):
        if not self.collected:
            # Create bobbing effect
            bob_offset = math.sin(self.bob_timer) * 3
            y_pos = self.y + bob_offset
            
            # Draw as a diamond shape
            points = [
                (self.x, y_pos - self.size//2),
                (self.x + self.size//2, y_pos),
                (self.x, y_pos + self.size//2),
                (self.x - self.size//2, y_pos)
            ]
            pygame.draw.polygon(screen, self.color, points)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro 2D Top-Down Game")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = [
            Enemy(100, 100),
            Enemy(SCREEN_WIDTH - 100, 100),
            Enemy(100, SCREEN_HEIGHT - 100)
        ]
        self.collectibles = [
            Collectible(200, 200),
            Collectible(600, 200),
            Collectible(400, 400),
            Collectible(200, 500)
        ]
        
        self.state = GameState()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_p:
                    self.state.paused = not self.state.paused
                if event.key == pygame.K_r and self.state.game_over:
                    self.restart_game()
        
        return True
    
    def update(self, dt):
        if self.state.paused or self.state.game_over:
            return
        
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(dt, keys)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player)
        
        # Update collectibles
        for collectible in self.collectibles:
            collectible.update(dt)
        
        # Check collisions
        self.check_collisions()
        
        # Check win condition
        if all(c.collected for c in self.collectibles):
            self.state.score += 100
            self.next_level()
    
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
    
    def next_level(self):
        self.state.level += 1
        # Add more enemies
        self.enemies.append(Enemy(50, 50))
        self.enemies.append(Enemy(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50))
        
        # Reset collectibles
        for collectible in self.collectibles:
            collectible.collected = False
        
        # Heal player a bit
        self.player.health = min(self.player.max_health, self.player.health + 25)
    
    def restart_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = [
            Enemy(100, 100),
            Enemy(SCREEN_WIDTH - 100, 100),
            Enemy(100, SCREEN_HEIGHT - 100)
        ]
        for collectible in self.collectibles:
            collectible.collected = False
        
        self.state = GameState()
    
    def draw_ui(self):
        # Score
        score_text = self.font.render(f"Score: {self.state.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Level
        level_text = self.font.render(f"Level: {self.state.level}", True, WHITE)
        self.screen.blit(level_text, (10, 50))
        
        # Health bar
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = 90
        
        # Background
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_width, health_height))
        
        # Health
        current_health_width = int((self.player.health / self.player.max_health) * health_width)
        pygame.draw.rect(self.screen, GREEN, (health_x, health_y, current_health_width, health_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (health_x, health_y, health_width, health_height), 2)
        
        # Health text
        health_text = self.small_font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y + health_height + 5))
        
        # Instructions
        if not self.state.game_over:
            instructions = [
                "WASD/Arrow Keys: Move",
                "P: Pause",
                "ESC: Quit",
                "Collect yellow diamonds!",
                "Avoid red enemies!"
            ]
            for i, instruction in enumerate(instructions):
                text = self.small_font.render(instruction, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 25))
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        if not self.state.game_over:
            self.player.draw(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            for collectible in self.collectibles:
                collectible.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw pause screen
        if self.state.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        
        # Draw game over screen
        if self.state.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(RED)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.state.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()