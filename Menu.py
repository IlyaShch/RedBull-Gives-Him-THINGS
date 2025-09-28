import pygame


class Menu:
    def __init__(self, screen, title, options=None, background_img=None, background_rect=None, coder_frames=None):
        self.screen = screen
        self.title = title
        self.options = options if options else ["Restart", "Quit"]
        self.font_title = pygame.font.Font(None, 96)
        self.font_option = pygame.font.Font(None, 48)
        self.selected_index = 0
        self.background_img = background_img
        self.background_rect = background_rect
        self.coder_frames = coder_frames or []
        self.coder_frame_idx = 0
        self.coder_anim_timer = 0
        self.coder_anim_speed = 0.10  # seconds per frame (faster typing)

    def draw(self):
        self.screen.fill((0, 0, 0))  # black background
        # Draw background image if provided
        if self.background_img is not None:
            bg = self.background_img.copy()
            bg.set_alpha(255)
            self.screen.blit(bg, self.background_rect)

        # --- Draw coder animation to the right of the title image ---
        if self.coder_frames:
            # Animate frame
            self.coder_anim_timer += 1/60  # assuming 60 FPS
            if self.coder_anim_timer >= self.coder_anim_speed:
                self.coder_anim_timer = 0
                self.coder_frame_idx = (self.coder_frame_idx + 1) % len(self.coder_frames)
            coder_img = self.coder_frames[self.coder_frame_idx]
            # Position: right of title image (move a bit left)
            coder_rect = coder_img.get_rect()
            coder_rect.midleft = (self.screen.get_width()//2 + 160, 250)
            self.screen.blit(coder_img, coder_rect)

        # --- Draw title if not empty ---
        if self.title:
            title_surface = self.font_title.render(self.title, True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(title_surface, title_rect)

        # --- Draw menu options ---
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            option_surface = self.font_option.render(option, True, color)
            option_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, 400 + i * 60))
            self.screen.blit(option_surface, option_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]  # return chosen option
        return None
