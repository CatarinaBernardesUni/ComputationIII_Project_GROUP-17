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
    cutefont = pygame.font.SysFont("Arial", 50)
    

    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    # displaying my background
    screen.blit(background, (0, 0))
    screen.blit(store_owner, store_owner_position)

    clock = pygame.time.Clock()

    # creating an event loop
    running = True
    while running:
        clock.tick(fps)

        # allowing the user to quit even tho they shouldn't because our game is perfect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # updating the display
        pygame.display.update()