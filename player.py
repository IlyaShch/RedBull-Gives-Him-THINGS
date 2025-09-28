import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200  # pixels per second

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
        # Make hitbox smaller (70% of sprite size)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.3, -self.rect.height * 0.3)


    def update(self, dt, keys):
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

        # Move player with screen bounds checking
        self.x = max(self.rect.width//2, min(SCREEN_WIDTH - self.rect.width//2, self.x + dx))
        self.y = max(self.rect.height//2, min(SCREEN_HEIGHT - self.rect.height//2, self.y + dy))
        self.rect.center = (self.x, self.y)
        self.hitbox.center = self.rect.center

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
        screen.blit(self.image, self.rect)
        # For debugging: draw hitbox
        # pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

    def get_rect(self):
        return self.hitbox
