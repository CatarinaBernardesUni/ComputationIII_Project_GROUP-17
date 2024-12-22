import pygame.display
import pygame.image
from game import *
from utils import *


def interface():
    """
    Handles the game interface setup and main menu interactions such as options, rules, quit, start game, and others.
    """
    # initiating pygame
    pygame.init()

    # changing the game icon
    pygame_icon = pygame.image.load("images/chests/chest_with_gold.png")
    pygame.display.set_icon(pygame_icon)
    # set the title of the window
    pygame.display.set_caption("Enchanted Forest")

    # initiating the music
    pygame.mixer.init()
    menu_music.play(-1)

    ########################### SETTING UP CURSOR ####################################
    # Load the custom cursor image, and loading the cursor to a bigger size
    cursor_image = pygame.transform.scale(pygame.image.load("mouse/mouse_trial.png"), (32, 32))

    # Create a surface for the cursor
    cursor_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))

    # creating a mandatory cursor object to be able to use it as a cursor later
    cursor = pygame.cursors.Cursor((0, 0), cursor_surface)

    # Set the custom cursor as our default
    pygame.mouse.set_cursor(cursor)

    ########################################################################
    # main interface loop (will run until the user quits)
    while True:

        # event detection (future work)
        for ev in pygame.event.get():

            mouse = pygame.mouse.get_pos()
            # seeing if the user hits the red x button
            if ev.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()

            # quit button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 548 <= mouse[0] <= 712 and 653 <= mouse[1] <= 709:
                    progress()
                    pygame.quit()
                    exit()

            # credits button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 800 <= mouse[0] < 975 and 514 <= mouse[1] < 573:
                    credits_()

            # play button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 517 <= mouse[0] <= 753 and 344 <= mouse[1] <= 429:
                    # wilderness_explorer()
                    # stopping the menu music
                    menu_music.stop()
                    # initializing the music for the main game
                    main_music.play(-1)
                    choose_character()

            # options button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 547 <= mouse[0] <= 719 and 517 <= mouse[1] <= 578:
                    options_menu()

            # rules button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 314 <= mouse[0] <= 472 and 521 <= mouse[1] <= 578:
                    rules_()

        # filling the screen
        bg = pygame.image.load("images/screens/menu.png")
        bg = pygame.transform.scale(bg, resolution)
        screen.blit(bg, (0, 0))
        # update the display so that the loop changes will appear
        pygame.display.update()


def rules_():
    """
    Handles the display and navigation of the game rules
    """
    page_1 = True
    screen.blit(rules_pages[0], (0, 0))
    current_index = 0
    while page_1:
        keys = pygame.key.get_pressed()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if current_index != 0:
                    screen.blit(rules_pages[current_index - 1], (0, 0))  # return from where it was before
                    current_index -= 1
                else:
                    interface()

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if current_index != 8:
                    # different from the index of the last page
                    screen.blit(rules_pages[current_index + 1], (0, 0))
                    current_index += 1

        pygame.display.update()
