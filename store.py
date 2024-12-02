from player import Player
from mouse_position import get_mouse_position, draw_button
import pygame
from config import *
from mouse_position import button_data, show_hover_message

def inside_store(player):

    # setting up a background
    store_owner = pygame.image.load("images/store/store_owner.png")
    store_owner = pygame.transform.scale(store_owner, (100, 100))
    store_owner_position = (600, 400)

    # setting up fonts for the text
    cutefont = pygame.font.Font("fonts/Minecraft.ttf", 30)

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
                exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.collidepoint(mouse):
                    shop_menu(player)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if quit_shop_button.collidepoint(mouse):
                    return

        # displaying my background
        screen.blit(entrance_store, (0, 0))
        screen.blit(store_owner, store_owner_position)

        shop_button = draw_button(screen, 255, 335, 190, 65, "shop", text_color=deep_black, image_path="images/store/store_button.png", font=cutefont)
        quit_shop_button = draw_button(screen, 475, 335, 245, 65, "leave shop", text_color=deep_black, image_path="images/store/store_button.png", font=cutefont)
        draw_button(screen, 255, 190, 450, 120, "welcome to the shop!", deep_black, "images/store/board.png", font=cutefont)

        # updating the display
        pygame.display.update()


def shop_menu(player):
    shopping = True
    custom_font = pygame.font.Font("fonts/Minecraft.ttf", 20)

    while shopping:
        screen.blit(entrance_store, (0, 0))
        screen.blit(menu_store, (width // 2 - 375, height // 2 - 300))
        # setting up so my gold amount shows on store menu
        gold_available = custom_font.render(f"My Gold: {player.gold}", True, brick_color)
        screen.blit(gold_available, (width // 2 - 310, height // 2 - 220))

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()

            # letting my player quit the game:
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # QUIT BUTTON
                if 946 <= mouse[0] <= 987 and 110 <= mouse[1] <= 152:
                    shopping = False
                # APPLE BUTTON
                if 348 <= mouse[0] <= 445 and 291 <= mouse[1] <= 334:
                    player.buy_item('apple')
                # MUSHROOM BUTTON
                if 509 <= mouse[0] <= 605 and 291 <= mouse[1] <= 334:
                    player.buy_item('mushroom')
                # POTION BUTTON
                if 670 <= mouse[0] <= 766 and 291 <= mouse[1] <= 334:
                    player.buy_item('speed potion')
                # SWORD BUTTON
                if 834 <= mouse[0] <= 930 and 291 <= mouse[1] <= 334:
                    player.buy_item('sword')
                # LAST ROW
                # DOG BUTTON
                if 347 <= mouse[0] <= 444 and 503 <= mouse[1] <= 546:
                    player.buy_item('dog')
                # SOUP BUTTON
                if 499 <= mouse[0] <= 600 and 503 <= mouse[1] <= 546:
                    player.buy_item('soup')
                # BOW BUTTON
                if 673 <= mouse[0] <= 767 and 503 <= mouse[1] <= 546:
                    player.buy_item('bow')
                # KEY BUTTON
                if 832 <= mouse[0] <= 926 and 500 <= mouse[1] <= 543:
                    player.buy_item('key')

        mouse_pos = get_mouse_position()
        for button in button_data.values():
            show_hover_message(screen, mouse_pos, button["rect"], button["description"])

        pygame.display.update()