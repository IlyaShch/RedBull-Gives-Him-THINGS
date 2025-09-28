def render_multiline_text(text, font, color, center, surface, line_spacing=8):
    # Helper to render multiline text centered
    lines = []
    words = text.split()
    max_width = 900
    while words:
        line_words = []
        while words:
            line_words.append(words.pop(0))
            test_line = ' '.join(line_words + words[:1])
            if font.size(test_line)[0] > max_width:
                break
        lines.append(' '.join(line_words))
    total_height = sum([font.size(line)[1] for line in lines]) + (len(lines)-1)*line_spacing
    y = center[1] - total_height//2
    for line in lines:
        rendered = font.render(line, True, color)
        rect = rendered.get_rect(center=(center[0], y + rendered.get_height()//2))
        surface.blit(rendered, rect)
        y += rendered.get_height() + line_spacing
def play_intro_sequence(screen, clock):
    # Load Jimmy frames (use first frame for intro)
    jimmy_img = pygame.image.load("Jimmy1.png").convert_alpha()
    jimmy_img = pygame.transform.scale(jimmy_img, (int(jimmy_img.get_width()*3.5), int(jimmy_img.get_height()*3.5)))
    brother_img = pygame.image.load("coder1.png").convert_alpha()
    brother_img = pygame.transform.scale(brother_img, (int(brother_img.get_width()*5.5), int(brother_img.get_height()*5.5)))

    # Fade in Jimmy
    fade_surface = pygame.Surface((1200, 900), pygame.SRCALPHA)
    alpha = 0
    fade_in_speed = 2  # slower fade in
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        fade_surface.fill((0,0,0,0))
        jimmy_img.set_alpha(alpha)
        fade_surface.blit(jimmy_img, jimmy_img.get_rect(center=(400, 500)))
        screen.blit(fade_surface, (0,0))
        pygame.display.flip()
        alpha = min(255, alpha + fade_in_speed)
        clock.tick(60)

    # Show Jimmy's speech
    font = pygame.font.Font(None, 54)
    jimmy_text = "I really want to win a HackUMBC. Brother Help!"
    skip = False
    for _ in range(180):  # show Jimmy's speech longer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                skip = True
        screen.fill((0,0,0))
        jimmy_img.set_alpha(255)
        screen.blit(jimmy_img, jimmy_img.get_rect(center=(400, 500)))
        render_multiline_text(jimmy_text, font, (255,255,255), (600, 200), screen)
        pygame.display.flip()
        clock.tick(60)
        if skip:
            break

    # Fade in brother
    alpha = 0
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        jimmy_img.set_alpha(255)
        brother_img.set_alpha(alpha)
        screen.blit(jimmy_img, jimmy_img.get_rect(center=(400, 500)))
        screen.blit(brother_img, brother_img.get_rect(center=(800, 500)))
        pygame.display.flip()
        alpha = min(255, alpha + fade_in_speed)
        clock.tick(60)

    # Show brother's speech
    brother_text = "I can win this for you, but I need you to bring me as many redbulls as you can to fuel me."
    skip = False
    for _ in range(240):  # show brother's speech longer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                skip = True
        screen.fill((0,0,0))
        screen.blit(jimmy_img, jimmy_img.get_rect(center=(400, 500)))
        screen.blit(brother_img, brother_img.get_rect(center=(800, 500)))
        render_multiline_text(brother_text, font, (255,255,0), (600, 300), screen)
        pygame.display.flip()
        clock.tick(60)
        if skip:
            break

    # Fade out to menu
    for alpha in range(0, 256, 4):  # slower fade out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        overlay = pygame.Surface((1200, 900))
        overlay.set_alpha(alpha)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        pygame.display.flip()
        clock.tick(60)

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

    # --- Intro Sequence ---
    play_intro_sequence(screen, clock)

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