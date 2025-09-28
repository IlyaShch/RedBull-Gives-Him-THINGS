import sys
import math
import pygame

from gamestate import GameState
from player import Player
from enemy import Enemy
from collectible import Collectible
from tilemap import TileMap

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
        self.deactive_collectible_index=-1

        #add the map class
        self.tilemap = TileMap(tile_size=48)

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
        
        for wall in self.tilemap.walls:
            if self.player.get_rect().colliderect(wall):
                # Compute overlap on each side
                dx_left   = self.player.rect.right - wall.left
                dx_right  = wall.right - self.player.rect.left
                dy_top    = self.player.rect.bottom - wall.top
                dy_bottom = wall.bottom - self.player.rect.top

                # Pick the smallest overlap (shallowest penetration)
                min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

                if min_overlap == dx_left:
                    self.player.rect.right = wall.left
                elif min_overlap == dx_right:
                    self.player.rect.left = wall.right
                elif min_overlap == dy_top:
                    self.player.rect.bottom = wall.top
                elif min_overlap == dy_bottom:
                    self.player.rect.top = wall.bottom

                # Sync player.x, player.y back to the rect center
                self.player.x, self.player.y = self.player.rect.center
        for enemy in self.enemies:
            enemy.update(dt, self.player)
            # --- enemy vs walls (push out using smallest-overlap side) ---


            # erect = enemy.get_rect()
            # for wall in self.tilemap.walls:
            #     if erect.colliderect(wall):
            #         dx_left   = erect.right  - wall.left
            #         dx_right  = wall.right   - erect.left
            #         dy_top    = erect.bottom - wall.top
            #         dy_bottom = wall.bottom  - erect.top

            #         min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

            #         if min_overlap == dx_left:
            #             erect.right = wall.left
            #         elif min_overlap == dx_right:
            #             erect.left = wall.right
            #         elif min_overlap == dy_top:
            #             erect.bottom = wall.top
            #         else:  # dy_bottom
            #             erect.top = wall.bottom

            #         # write the corrected position back to the enemy
            #         enemy.x, enemy.y = erect.center
            # --- enemy slows down if colliding with wall ---
            if any(enemy.get_rect().colliderect(wall) for wall in self.tilemap.walls):
                # optional: reduce speed factor so they crawl while stuck
                enemy.speed = 25
            else:
                enemy.speed = 50  # normal speed
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
             # --- draw map ---
            self.tilemap.draw(self.screen)
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
        for i in range(0,len(self.collectibles)):
            if i!=self.deactive_collectible_index and player_rect.colliderect(self.collectibles[i].get_rect()):
                self.collectibles[i].collected = True
                self.state.score += 10  # <-- add 10 for collectible
                for other in self.collectibles:
                    #if other!=self.collectibles[i]:
                    self.collectibles[i].collected=False
                self.deactive_collectible_index=i
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