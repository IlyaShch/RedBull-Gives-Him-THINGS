import sys
import math
import pygame
import random


from gamestate import GameState
from player import Player
from enemy import Enemy
from collectible import Collectible
from tilemap import TileMap
from progressbar import ProgressBar
from musichandler import MusicHandler

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
        self.enemies = [
            Enemy(100,100),
            Enemy(1100, 100, image_paths=["dog.webp", "dog.webp"], scale=0.5, dialogue="woof", anim_speed=0.1),
            Enemy(400, 400, image_paths=["coder1.png", "coder2.png"], scale=0.5, anim_speed=0.1)
        ]
        self.collectibles = [Collectible(400,300), Collectible(800,600)]
        self.running = True
        self.state = GameState()
        self.font = pygame.font.Font(None, 36)       # Big font for score
        self.small_font = pygame.font.Font(None, 24) # Smaller font for health
        self.deactive_collectible_index=-1

        #add the map class
        self.tilemap1 = TileMap(layout=[
            "WWWWWWWWWWWWWWWWWWWWWWWW",
            "W....W.....EE....W......",
            "W....W...........W......",
            "W..WWW...........WWW....",
            "W........WWWWW..........",
            "W........W...W.........D",
            "W........W..WW.........D",
            "W...............WW.W....",
            "WZZ.............W..W....",
            "WZZ.............WW.W....",
            "........................",
            "......................WW",
            "......................WW",
            "......................WW",
            "......................WW",
            "......................WW",
            "......................WW",
            "......................WW"
        ], tile_size=48)

        self.tilemap2 = TileMap(layout=
            [
            "WWWWWWWWWWWWWWWWWWWWWWWW",
            "W..................DD..W",
            "W......................W",
            "W......................W",
            "WE.....................W",
            "WE........W............W",
            "W......................W",
            "W......................W",
            "W.............W........W",
            "W..WW..................W",
            "W......................W",
            "W......................W",
            "W......................W",
            "W........W.............W",
            "W......................W",
            "W......................W",
            "W......................W",
            "WWWWWWWWWWWWWWWWWWWWWWWW"
        ], tile_size=48)

        self.tilemap3 = TileMap(layout=[
            "WWWWWWWWWWWWWWWWWWWWWWWW",
            "W.............W........W",
            "W..WWW.............W...W",
            "W..W.............W.....W",
            "W..W........W....W.....W",
            "W..W.............W.....W",
            "W..WWW..WW..W.W..WWW...W",
            "W......................W",
            "WD..............WW.....W",
            "WD...W..W......W..W....W",
            "W....W..W......W..W....W",
            "W...............WWW....W",
            "W......................W",
            "W..W....W......WWW.....W",
            "W...........W........W.W",
            "W...........W..........W",
            "W.............W...EE...W",
            "WWWWWWWWWWWWWWWWWWWWWWWW"
        ], tile_size=48)

        self.tilemap4 = TileMap(layout=[
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "W............WW.....W...W",
            "W.............W.....W...W",
            "W.............W....WWW..W",
            "W..W...............W....W",
            "W..W..............W......",
            "W..W..............W......",
            "W.............W.W.......E",
            "W........W..............E",
            "W........W........W.W...W",
            "W........W..........W...W",
            "W....WWW......WWW.W.W...W",
            "W................W.......",
            "W..WWW..WWW........WWW..W",
            "W..W........W..........W.",
            "W..W........W..........W.",
            "W.................DD.....",
            "WWWWWWWWWWWWWWWWWWWWWWWWW"
        ], tile_size=48)

        self.tilemap1.add_target1(self.tilemap2)
        self.tilemap2.add_target1(self.tilemap3)
        self.tilemap3.add_target1(self.tilemap4)
        self.tilemap4.add_target1(self.tilemap1)

        self.tilemap1.add_target2(self.tilemap4)
        self.tilemap2.add_target2(self.tilemap1)
        self.tilemap3.add_target2(self.tilemap2)
        self.tilemap4.add_target2(self.tilemap3)

        # Start with the first map
        self.tilemap = self.tilemap1

        # Music handler: loop 'casual-panic_X7OnO11p.wav' forever
        self.music = MusicHandler("casual-panic_X7OnO11p.wav")
        self.music.play(loops=-1)
        # Load SFX for dropzone
       # self.music.load_sound("drink", "drink.wav")
        self.music.load_sound("pop", "popppp.wav")

        # Progress bars
        self.progress_yellow = ProgressBar(10, 80, 300, 24, (255, 255, 0))
        self.progress_blue = ProgressBar(10, 120, 300, 24, (0, 180, 255))
        #self.progress_blue.initial_progress()
        self.progress_blue.fullness = 0.0  # Demo value, you can link to another variable

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r and self.state.game_over:
                    self.restart_game()
            #if event.type == pygame.USEREVENT + 1:
            #    self.music.play_sound("drink")

    def update(self, dt):
        if self.player is None:
            print("[DEBUG] Player is None")
        if self.collectibles is None:
            print("[DEBUG] Collectibles is None")
        if self.enemies is None:
            print("[DEBUG] Enemies is None")
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
        for door_rect in self.tilemap.doors1:
            if self.player.get_rect().colliderect(door_rect):
                #if self.tilemap.door1:
                self.tilemap = self.tilemap.door1
                # Reset player to top-left
                self.player.x, self.player.y = 100, 100
                self.player.rect.center = (self.player.x, self.player.y)
                break
        
        for door_rect in self.tilemap.doors2:
            if self.player.get_rect().colliderect(door_rect):
                #if self.tilemap.door1:
                self.tilemap = self.tilemap.door2
                # Reset player to top-left
                self.player.x, self.player.y = 100, 100
                self.player.rect.center = (self.player.x, self.player.y)
                break


                    # --- NEW: dropzone interaction ---
        # --- NEW: dropzone interaction ---
        for dz in self.tilemap.dropzones:
            if self.player.get_rect().colliderect(dz):
                if self.state.inventory > 0:
                    print(f"Dropped off {self.state.inventory} Red Bulls!")
                    self.state.stash += self.state.inventory  # bank them
                    self.progress_yellow.fullness += (0.2 * self.state.inventory)
                    self.state.inventory = 0
                    # Play two SFX in sequence
                    self.music.play_sound("pop")
                    # Schedule the second sound to play after the first finishes
                   #  pop_length = self.music.sounds["pop"].get_length()
                    # pygame.time.set_timer(pygame.USEREVENT + 1, int(pop_length * 1000), loops=1)
        

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
        
        if self.state.game_over==False:
            self.check_collisions()

        #self.state.time_left -= dt
        #if self.state.time_left <= 0:
        if self.progress_yellow.fullness <=0:
            self.state.time_left = 0
            self.state.game_over = True
            #self.clear()

    #def load_map(self, map_name):
        # 1. Load new map
        #self.tilemap.load_map(map_name)   # you'll need a load_map method in TileMap

        # 2. Move player to new position
        #self.player.x, self.player.y = player_pos
        #self.player.rect.center = player_pos

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
                if not collectible.collected:
                    collectible.draw(self.screen)
                                
        # Draw UI on top
        self.draw_ui()
        
        # Draw game over overlay
        if self.state.game_over:
            if self.state.stash > self.state.high_score:
                self.state.high_score = self.state.stash
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)  # semi-transparent black
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            go_text = self.font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(go_text, go_rect)
            
            # Current score
            score_text = self.font.render(f"Score: {self.state.stash}", True, WHITE)
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
        
        # --- Enemy collisions ---
        if len(self.enemies)>0:
            for enemy in self.enemies[:]:
                if player_rect.colliderect(enemy.get_rect()):
                    if self.state.inventory > 0:
                        self.state.inventory =0
                    print(f"Hit enemy! Inventory: {self.state.inventory}")
                    self.enemies.remove(enemy)
                    print(self.enemies)

        # --- Collectible collisions ---
        if len(self.collectibles)>0:
            for collectible in self.collectibles:
                if not collectible.collected and player_rect.colliderect(collectible.get_rect()):
                    collectible.collected = True
                    self.state.inventory += 1
                    self.player.speed = 1.25 * self.player.speed  # speed boost on pickup
                    print(f"Collected! Red Bull: {self.state.inventory}, New speed: {self.player.speed}")


            # --- Reset all collectibles if all collected ---
        if all(c.collected for c in self.collectibles):
            print("All Red Bulls collected! Resetting collectibles...")
            self.randomize_collectibles()
            for c in self.collectibles:
                c.collected = False
                
    def draw_ui(self):
        # --- Score display ---
        score_text = self.font.render(f"Stash Size: {self.state.stash}", True, YELLOW)
        self.screen.blit(score_text, (10, 10))

        # --- Inventory display ---
        inventory_text = self.font.render(f"Inventory: {self.state.inventory}", True, RED)
        self.screen.blit(inventory_text, (10, 40))

        # --- Progress bars ---
        time_fullness = max(0.0, min(1.0, self.state.time_left / 10))  # assuming 10s max
        self.progress_yellow.subtract_fullness(0.001)
        self.progress_yellow.draw(self.screen)

        # Blue bar: demo, decrease over time for now
        #self.progress_blue.fullness = min(1, self.progress_blue.fullness + 0.002)
        self.progress_blue.add_fullness(0.001)
        #self.progress_blue.set_fullness(self.progress_blue.fullness)
        self.progress_blue.draw(self.screen)

        timer_text = self.font.render(f"Time Left: {int(self.state.time_left)}s", True, CYAN)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 250, 10))

            
    #def reset_collectibles(self, index):
    #    for i in range(0,len(self.collectibles)):
    #        if i!=index:
    #            self.collectibles[i].collected=False

    def restart_game(self):
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.enemies = [Enemy(100, 100), Enemy(1100, 100)]
        for collectible in self.collectibles:
            collectible.collected = False
        self.state.game_over = False
        self.state.game_won = False
        self.state.stash = 0
        self.state.inventory =0
        self.state.time_left = 10
        self.randomize_collectibles()
        self.progress_blue.fullness=0
        self.progress_yellow.fullness=1
    
    def clear(self):
        self.collectible=[]
        self.enemies=[]

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()

    def randomize_collectibles(self):
        for collectible in self.collectibles:
            while True:
                # Generate random coordinates within screen bounds
                x = random.randint(collectible.rect.width // 2, SCREEN_WIDTH - collectible.rect.width // 2)
                y = random.randint(collectible.rect.height // 2, SCREEN_HEIGHT - collectible.rect.height // 2)
                
                # Check collision with walls
                rect = pygame.Rect(x - collectible.rect.width//2, y - collectible.rect.height//2,
                                collectible.rect.width, collectible.rect.height)
                if not any(rect.colliderect(wall) for wall in self.tilemap.walls):
                    # Valid position found
                    collectible.x = x
                    collectible.y = y
                    collectible.rect.center = (x, y)
                    break