import math
import pygame

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


class Entity:
    def __init__(self, x, y, image_paths=None, scale=1.0, dialogue="", anim_speed=1.0):
        self.x = x
        self.y = y
  #      self.image = None
        self.dialogue = dialogue  # String field for enemy dialogue or label
        self.anim_speed = anim_speed
        self.frames = []
        
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

    def animate(self, dt):
        if self.frames:
            self.frame_timer += dt * self.anim_speed
            if self.frame_timer > self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.rect.center = (self.x, self.y)


    def draw(self, screen):
        if self.frames:
            # Use animated frames
            screen.blit(self.frames[self.current_frame], self.rect)
   #     elif self.image:
     #       screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, (self.x-8, self.y-8, 16, 16))

    def get_rect(self):
#        if self.image:
   #         return self.rect
        return pygame.Rect(self.x-8, self.y-8, 16, 16)