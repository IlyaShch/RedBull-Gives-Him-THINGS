import math
import pygame

from entity import Entity

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


class Enemy(Entity):
    def __init__(self, x, y, image_paths=None, scale=1.0, dialogue="", anim_speed=1.0):
        super().__init__(x=x, y=y, image_paths=image_paths, scale=scale, dialogue=dialogue, anim_speed=anim_speed)
        self.size = 16
        self.base_speed = 50
        self.speed = self.base_speed
        self.color = RED
        self.rect = None

        # Charge logic
        self.charge_timer = 0
        self.charge_cooldown = 2.5 + 2.5 * (pygame.time.get_ticks() % 1000) / 1000  # randomize interval
        self.charge_duration = 1.2 + 0.8 * (pygame.time.get_ticks() % 1000) / 1000  # randomize charge length
        self.charging = False
        self.charge_dir = (0, 0)

        if image_paths:
            for path in image_paths:
                img_temp = pygame.image.load(path).convert_alpha()
                width = int(img_temp.get_width() * scale)
                height = int(img_temp.get_height() * scale)
                frame = pygame.transform.smoothscale(img_temp, (width, height))
                self.frames.append(frame)
            self.current_frame = 0
            self.frame_timer = 0
            self.frame_duration = 0.15  # seconds per frame (base)
            self.rect = self.frames[0].get_rect(center=(self.x, self.y))
        else:
            self.frames = None
            self.rect = None

    def update(self, dt, player):
        # Charging logic: randomly charge a long distance in a straight line
        if self.charging:
            self.charge_timer -= dt
            self.speed = self.base_speed * 3.2
            dx, dy = self.charge_dir
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
            if self.charge_timer <= 0:
                self.charging = False
                self.charge_cooldown = 2.0 + 2.5 * (pygame.time.get_ticks() % 1000) / 1000
        else:
            self.charge_cooldown -= dt
            self.speed = self.base_speed
            # Normal tracking
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if self.charge_cooldown <= 0:
                # Start a charge in a random direction (sometimes toward player, sometimes random)
                import random
                if random.random() < 0.6:
                    # 60% chance: charge toward player
                    if dist > 0:
                        dir_x = dx / dist
                        dir_y = dy / dist
                    else:
                        dir_x, dir_y = 1, 0
                else:
                    # 40% chance: random direction
                    angle = random.uniform(0, 2*math.pi)
                    dir_x = math.cos(angle)
                    dir_y = math.sin(angle)
                self.charge_dir = (dir_x, dir_y)
                self.charging = True
                self.charge_timer = self.charge_duration
            elif dist > 0:
                self.x += (dx / dist) * self.speed * dt
                self.y += (dy / dist) * self.speed * dt
        super().animate(dt)