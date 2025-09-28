
import pygame
import math
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_speed = 200  # normal speed
        self.speed = self.base_speed
        self.boost_speed = 350  # speed during boost
        self.boost_duration = 0.25  # seconds
        self.boost_timer = 0

        # Particle system for boost
        self.particles = []  # Each particle: [x, y, vx, vy, life, max_life, color, radius]

        # Load and scale jimmy sprites
        self.jimmy_frames = []
        scale_factor = 3.5
        for fname in ["jimmy1.png", "jimmy2.png", "jimmy3.png"]:
            img = pygame.image.load(fname).convert_alpha()
            width = int(img.get_width() * scale_factor)
            height = int(img.get_height() * scale_factor)
            self.jimmy_frames.append(pygame.transform.scale(img, (width, height)))
        self.jimmy_frame_idx = 0
        self.jimmy_anim_timer = 0
        self.jimmy_anim_speed = 0.12  # seconds per frame
        self.facing_left = False
        self.image = self.jimmy_frames[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    # Make hitbox even smaller (50% of sprite size)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)


    def update(self, dt, keys, walls=None):
        # Handle boost
        if keys[pygame.K_SPACE]:
            if self.boost_timer <= 0:
                self.boost_timer = self.boost_duration
        if self.boost_timer > 0:
            self.speed = self.boost_speed
            self.boost_timer -= dt
            if self.boost_timer <= 0:
                self.speed = self.base_speed
        else:
            self.speed = self.base_speed

        # Emit particles if boosting
        if self.boost_timer > 0:
            for _ in range(7):  # Emit more particles per frame for longer trail
                angle = random.uniform(-0.7, 0.7)
                speed = random.uniform(70, 160)
                vx = math.cos(angle + math.pi) * speed
                vy = math.sin(angle + math.pi) * speed
                px = self.x + random.uniform(-8, 8)
                py = self.y + self.rect.height//4 + random.uniform(-8, 8)
                max_life = random.uniform(0.35, 0.55)  # longer life
                # Sparkly color: random yellow/white
                if random.random() < 0.5:
                    color = (255, 255, random.randint(80, 180))
                else:
                    color = (255, 255, 255)
                radius = random.randint(2, 6)
                self.particles.append([px, py, vx, vy, 0, max_life, color, radius])

        # Update particles
        for p in self.particles:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[4] += dt
        self.particles = [p for p in self.particles if p[4] < p[5]]

        dx = dy = 0
        moving = False
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        if left:
            dx = -self.speed * dt
            moving = True
            self.facing_left = False
        if right:
            dx = self.speed * dt
            moving = True
            self.facing_left = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed * dt
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed * dt
            moving = True

        # Move and check collisions (AABB, axis-aligned)
        if walls is None:
            walls = []
        # Move on x axis
        new_x = self.x + dx
        self.rect.centerx = int(new_x)
        self.hitbox.centerx = self.rect.centerx
        collided_x = False
        for wall in walls:
            if self.get_rect().colliderect(wall):
                collided_x = True
                break
        if not collided_x:
            self.x = new_x
        self.rect.centerx = int(self.x)
        self.hitbox.centerx = self.rect.centerx

        # Move on y axis
        new_y = self.y + dy
        self.rect.centery = int(new_y)
        self.hitbox.centery = self.rect.centery
        collided_y = False
        for wall in walls:
            if self.get_rect().colliderect(wall):
                collided_y = True
                break
        if not collided_y:
            self.y = new_y
        self.rect.centery = int(self.y)
        self.hitbox.centery = self.rect.centery

        # Animate if moving
        if moving:
            self.jimmy_anim_timer += dt
            if self.jimmy_anim_timer >= self.jimmy_anim_speed:
                self.jimmy_anim_timer = 0
                self.jimmy_frame_idx = (self.jimmy_frame_idx + 1) % len(self.jimmy_frames)
        else:
            self.jimmy_frame_idx = 0
        base_img = self.jimmy_frames[self.jimmy_frame_idx]
        if self.facing_left:
            self.image = pygame.transform.flip(base_img, True, False)
        else:
            self.image = base_img

    def draw(self, screen):
        # Draw particles behind player
        for p in self.particles:
            alpha = max(0, 255 - int((p[4]/p[5])*255))
            color = (*p[6], alpha)
            radius = max(1, int(p[7] * (1 - p[4]/p[5])))
            surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (radius, radius), radius)
            # Add sparkly effect: draw a small white core
            if radius > 2:
                core_radius = max(1, radius // 2)
                pygame.draw.circle(surf, (255,255,255, min(255, alpha+80)), (radius, radius), core_radius)
            screen.blit(surf, (p[0]-radius, p[1]-radius))
        screen.blit(self.image, self.rect)
        # For debugging: draw hitbox
        # pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

    def get_rect(self):
        return self.hitbox
