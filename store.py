from player import *
from config import *
from visual import *
from mouse_position import *
import pygame
from shed import *


def inside_store(player):
    # setting up a background
    background = pygame.image.load("images/store_front.png")
    background = pygame.transform.scale(background, resolution)
    store_owner = pygame.image.load("images/store_owner.png")
    store_owner = pygame.transform.scale(store_owner, (100, 100))
    store_owner_position = (600, 400)

    # setting up fonts for the text
    cutefont = pygame.font.SysFont("American Typewriter", 50)
    lady_text = cutefont.render("Welcome to our store! "
                                "Are you looking to buy?", True, white)


    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    clock = pygame.time.Clock()

    shop_button = None
    quit_shop_button = None

    # creating an event loop
    running = True
    while running:
        mouse = get_mouse_position()
        clock.tick(fps)

        # allowing the user to quit even tho they shouldn't because our game is perfect
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.collidepoint(mouse):
                    shop_time(player)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if quit_shop_button.collidepoint(mouse):
                    return

        # displaying my background
        screen.blit(background, (0, 0))
        screen.blit(store_owner, store_owner_position)

        shop_button = draw_button(screen, 255, 335, 190, 65, "shop", text_color=white, image_path="images/store_button.png")
        quit_shop_button = draw_button(screen, 475, 335, 245, 65, "leave shop", text_color=white, image_path="images/store_button.png")
        draw_button(screen, 255, 190, 450, 120, "welcome to my shop!", white, "images/board.png")

        # updating the display
        pygame.display.update()


def shop_time(player):
    pass