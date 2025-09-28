
import pygame
import sys
import math
import os


from game import Game
from tilemap import TileMap
from Menu import Menu

pygame.init()


if __name__ == "__main__":
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()

    # --- Fade-in Title Screen ---
    title_img = pygame.image.load("Titile.png").convert_alpha()
    # Scale up (e.g., 2x)
    scale_factor = 7.5
    w, h = title_img.get_width(), title_img.get_height()
    scaled_img = pygame.transform.scale(title_img, (int(w*scale_factor), int(h*scale_factor)))
    img_rect = scaled_img.get_rect(center=(600, 250))
    fade_surface = pygame.Surface((1300, 900), pygame.SRCALPHA)
    alpha = 0
    fade_in_speed = 3  # Higher is faster
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        fade_surface.fill((0,0,0,0))
        scaled_img.set_alpha(alpha)
        fade_surface.blit(scaled_img, img_rect)
        screen.blit(fade_surface, (0,0))
        pygame.display.flip()
        alpha = min(255, alpha + fade_in_speed)
        clock.tick(60)

    # Hold the title for a moment
    hold_time = 60  # frames
    for _ in range(hold_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        scaled_img.set_alpha(255)
        screen.blit(scaled_img, img_rect)
        pygame.display.flip()
        clock.tick(60)

    # --- Main Menu ---
    # Load coder frames and scale them
    coder1 = pygame.image.load("coder1.png").convert_alpha()
    coder2 = pygame.image.load("coder2.png").convert_alpha()
    coder_scale = 8.5
    coder1 = pygame.transform.scale(coder1, (int(coder1.get_width()*coder_scale), int(coder1.get_height()*coder_scale)))
    coder2 = pygame.transform.scale(coder2, (int(coder2.get_width()*coder_scale), int(coder2.get_height()*coder_scale)))
    coder_frames = [coder1, coder2]

    menu = Menu(screen, "", ["Start Game", "Instructions", "Quit"], background_img=scaled_img, background_rect=img_rect, coder_frames=coder_frames)
    show_menu = True
    selected_option = None
    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result = menu.handle_input(event)
            if result:
                selected_option = result
                if selected_option == "Start Game":
                    show_menu = False
                elif selected_option == "Instructions":
                    # Simple instructions overlay
                    instructions = True
                    while instructions:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                                instructions = False
                        menu.draw()
                        font = pygame.font.Font(None, 48)
                        text = font.render("Use arrow keys to move. Collect Red Bulls!", True, (255,255,255))
                        rect = text.get_rect(center=(600, 400))
                        screen.blit(text, rect)
                        text2 = font.render("Press ESC to return", True, (255,255,0))
                        rect2 = text2.get_rect(center=(600, 500))
                        screen.blit(text2, rect2)
                        pygame.display.flip()
                        clock.tick(60)
                elif selected_option == "Quit":
                    pygame.quit()
                    sys.exit()
        menu.draw()
        pygame.display.flip()
        clock.tick(60)
    # Start the game after menu
    game = Game()
    game.run()