import pygame.display
from game import *
from config import *
from utils import *
import platform


# from player import Player


def interface():
    # initiating pygame
    pygame.init()

    # changing the game icon
    pygame_icon = pygame.image.load("images/chests/chest_with_gold.png")
    pygame.display.set_icon(pygame_icon)
    # set the title of the window
    pygame.display.set_caption("Game Title")


    # initiating the music
    pygame.mixer.init()
    # load and play the music for the man menu
    pygame.mixer.music.load("music/main_menu.mp3")
    pygame.mixer.music.play(-1)  # -1 makes the music play in loop


    # creating the screen at the set resolution
    # screen = pygame.display.set_mode(resolution)  # show the user something

    # this was in the execute game function, I put it here to change the title of the window even if we
    # don't click in the "start game"

    ########################### SETTING UP CURSOR ####################################
    # Load the custom cursor image
    cursor_image = pygame.image.load("mouse/mouse_trial.png")

    #Loading the cursor to a bigger size
    cursor_image = pygame.transform.scale(cursor_image, (32, 32))

    # Create a surface for the cursor
    cursor_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))

    # creating a mandatory cursor object to be able to use it as a cursor later
    cursor = pygame.cursors.Cursor((0, 0), cursor_surface)

    # Set the custom cursor as our default
    pygame.mouse.set_cursor(cursor)

    ########################################################################

    # setting the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 50)

    # render the text (will be used in the game button)
    # wilderness_text = corbelfont.render("Wilderness Explorer", True, white)
    # quit_text = corbelfont.render("quit", True, white)
    # rules_text = corbelfont.render("rules", True, white)
    # options_text = corbelfont.render("options", True, white)
    # credits_text = corbelfont.render("credits", True, white)
    # title_text = comicsansfont.render("Computation III - Project", True, glowing_light_red)
    # main interface loop (will run until the user quits)
    while True:

        # event detection (future work)
        for ev in pygame.event.get():

            # getting the mouse position (future need)
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
                    interface()

            # wilderness game button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 517 <= mouse[0] <= 753 and 344 <= mouse[1] <= 429:
                    # wilderness_explorer()
                    # stopping the menu music
                    pygame.mixer.music.stop()
                    # initializing the music for the main game
                    pygame.mixer.music.load("music/Adventure.mp3")
                    pygame.mixer.music.play(-1)
                    choose_character()

            # options button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 547 <= mouse[0] <= 719 and 517 <= mouse[1] <= 578:
                    options_menu()

            # rules button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 314 <= mouse[0] <= 472 and 521 <= mouse[1] <= 578:
                    under_construction()
                    rules_()

        # cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
        # pygame.mouse.set_cursor((8, 16), (0, 0), *cursor)
        # filling the screen
        bg = pygame.image.load("images/screens/menu.png")
        bg = pygame.transform.scale(bg, resolution)
        screen.blit(bg, (0, 0))
        # wilderness explorer button
        # pygame.draw.rect(screen, dark_red, [90, 240, 540, 60])
        # wilderness_rect = wilderness_text.get_rect(center=(90 + 540 // 2, 240 + 60 // 2))  # text centered in the button
        # screen.blit(wilderness_text, wilderness_rect)

        # rules button
        # pygame.draw.rect(screen, grey, [90, 480, 140, 60])
        # rules_rect = rules_text.get_rect(center=(90 + 140 // 2, 480 + 60 // 2))  # text centered in the button
        # screen.blit(rules_text, rules_rect)

        # options button
        # pygame.draw.rect(screen, grey, [90, 600, 140, 60])
        # options_rect = options_text.get_rect(center=(90 + 140 // 2, 600 + 60 // 2))  # text centered in the button
        # screen.blit(options_text, options_rect)

        # quit button
        # pygame.draw.rect(screen, grey, [450, 600, 140, 60])
        # quit_rect = quit_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))  # text centered in the button
        # screen.blit(quit_text, quit_rect)

        # credits button
        # pygame.draw.rect(screen, grey, [450, 480, 140, 60])
        # credits_rect = credits_text.get_rect(center=(450 + 140 // 2, 480 + 60 // 2))  # text centered in the button
        # screen.blit(credits_text, credits_rect)

        # showing the title of the project
        # screen.blit(title_text, (55, 0))

        # update the display so that the loop changes will appear
        pygame.display.update()


def credits_():
    # screen = pygame.display.set_mode(resolution)

    # in order to print something we need to first create a font, create the text and then blit

    # creating the fonts:
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

    # creating the rendered texts for the credits
    augusto_text = comicsansfont.render("Augusto Santos, ajrsantos@novaims.unl.pt", True, white)
    diogo_text = comicsansfont.render("Diogo Rastreio, drasteiro@novaims.unl.pt", True, white)
    liah_text = comicsansfont.render("Liah Rosenfeld, lrosenfeld@novaims.unl.pt", True, white)

    # main loop to detect user input and display the credits
    while True:
        # getting the position of the users mouse
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()

            # checking if the user clicked the back button
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    interface()

        # display my screen
    screen.fill(deep_black)  # we can fill the screen with an image instead of deep_black
    # displaying our texts
    screen.blit(augusto_text, (0, 0))  # first line
    screen.blit(diogo_text, (0, 25))
    screen.blit(liah_text, (0, 50))

    # drawing and displaying the back button
    pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
    back_text = corbelfont.render("back", True, white)
    back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
    screen.blit(back_text, back_rect)

    # updating the display
    pygame.display.update()


def rules_():
    print("Displaying rules...")
