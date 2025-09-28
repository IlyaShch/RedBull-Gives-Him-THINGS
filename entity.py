
import math
import pygame
import random

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
    def __init__(self, x, y, image_paths=None, scale=1.0, dialogue="", anim_speed=1.0, show_speech=False):
        self.x = x
        self.y = y
  #      self.image = None
        self.dialogue = dialogue  # String field for enemy dialogue or label
        self.anim_speed = anim_speed
        self.frames = []
        self.show_speech = show_speech
        # Speech bubble support (only if show_speech is True)
        if self.show_speech:
            self.speech_lines_existential = [
                "Why am I even here?",
                "The caffeine can't fill the void...",
                "If I code all night, will I finally feel alive?",
                "My soul is as empty as my Red Bull can.",
                "What if the bug is inside me?",
                "I used to have dreams. Now I have deadlines.",
                "The compiler can't fix what's broken inside.",
                "I stare into the abyss, and it returns a stack trace."
            ]
            self.speech_lines_normal = [
                "I need more Red Bull!",
                "Planning my caffeine-induced heart attack.",
                "I can quit anytime... after this can.",
                "Red Bull is my co-pilot.",
                "Who needs blood when you have caffeine?"
            ]
            self.speech_lines_hyper = [
                "Even Donayee Can't Stop Me Now!",
                "Can you hear the shapes too?",
                "I can double major!",
                "I am on speed!",
                "I could pass CMSC 343!",
                "Who needs sleep when you have crack?"
            ]
            self.speech_timer = 0
            self.speech_interval = 3.5  # seconds between new lines
            self.current_speech = random.choice(self.speech_lines_normal)
            self._last_group = 'normal'
        else:
            self.speech_lines_existential = []
            self.speech_lines_normal = []
            self.speech_lines_hyper = []
            self.speech_timer = 0
            self.speech_interval = 0
            self.current_speech = ""
            self._last_group = None
        
        if image_paths:
            for path in image_paths:
                img_temp = pygame.image.load(path).convert_alpha()
                width = int(img_temp.get_width() * scale)
                height = int(img_temp.get_height() * scale)
                frame = pygame.transform.scale(img_temp, (width, height))
                self.frames.append(frame)
            self.current_frame = 0
            self.frame_timer = 0
            self.frame_duration = 0.15  # seconds per frame (base)
            self.rect = self.frames[0].get_rect(center=(self.x, self.y))
        else:
            self.frames = None
            self.rect = None

    def animate(self, dt, yellow_fullness=None):
        if self.frames:
            self.frame_timer += dt * self.anim_speed
            if self.frame_timer > self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.rect.center = (self.x, self.y)

        # Speech bubble timer (only if enabled)
        if self.show_speech:
            # Determine voiceline group based on yellow bar
            group = 'normal'
            if yellow_fullness is not None:
                if yellow_fullness < 0.5:
                    group = 'existential'
                elif yellow_fullness > 0.8:
                    group = 'hyper'
            lines = self.speech_lines_normal
            if group == 'existential':
                lines = self.speech_lines_existential
            elif group == 'hyper':
                lines = self.speech_lines_hyper
            # Only change line if group changes or timer expires
            self.speech_timer += dt
            if self.speech_timer > self.speech_interval or group != self._last_group:
                self.speech_timer = 0
                self.current_speech = random.choice(lines) if lines else ""
                self._last_group = group


    def draw(self, screen):
        if self.frames:
            # Use animated frames
            screen.blit(self.frames[self.current_frame], self.rect)
            # Draw speech bubble above entity (only if enabled)
            if self.show_speech and self.current_speech:
                font = pygame.font.Font(None, 28)
                text_surf = font.render(self.current_speech, True, (0,0,0))
                padding = 8
                bubble_w = text_surf.get_width() + padding*2
                bubble_h = text_surf.get_height() + padding*2
                bubble_surf = pygame.Surface((bubble_w, bubble_h), pygame.SRCALPHA)
                pygame.draw.rect(bubble_surf, (255,255,255,230), (0,0,bubble_w,bubble_h), border_radius=10)
                pygame.draw.rect(bubble_surf, (0,0,0,100), (0,0,bubble_w,bubble_h), 2, border_radius=10)
                bubble_surf.blit(text_surf, (padding, padding))
                # Position bubble above coder and clamp to screen
                bubble_x = self.rect.centerx - bubble_w//2
                bubble_y = self.rect.top - bubble_h - 10
                # Clamp horizontally
                bubble_x = max(0, min(bubble_x, SCREEN_WIDTH - bubble_w))
                # Clamp vertically (in case coder is near top)
                bubble_y = max(0, bubble_y)
                screen.blit(bubble_surf, (bubble_x, bubble_y))
        else:
            pygame.draw.rect(screen, self.color, (self.x-8, self.y-8, 16, 16))

    def get_rect(self):
#        if self.image:
   #         return self.rect
        return pygame.Rect(self.x-8, self.y-8, 16, 16)