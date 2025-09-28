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
        self.speed = 50
        self.color = RED
        self.rect = None

       
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
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt
        super().animate(dt)