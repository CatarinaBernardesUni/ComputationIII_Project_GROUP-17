from config import *
from pytmx.util_pygame import load_pygame
from mouse_position import button_data, show_hover_message, draw_button, get_mouse_position
from utils import area_setup


def inside_store(player):
    """
    Handles the logic of the player inside the store
    Sets up the inside of the store, including the leave and shop button.
    The loop handles the interaction within the store, such as going to shop_menu().

    Parameters
    ----------
    player: Player

    Returns
    -----------
    'main'
        if the player leaves the store returns 'main'
    """

    ################ TESTING THE TILES ###################
    store_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2, height // 2))
    clock = pygame.time.Clock()

    ############################### STORE MAP ################################

    tmx_data = load_pygame("data/WE STORE/WE STORE MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data, None, None, None, None)

    #####################################################################

    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # setting the player initial position on the store
    player.rect.center = (300, 320)
    player.state = "down"

    # creating an event loop
    running = True
    while running:
        mouse = get_mouse_position()
        # was giving an error bc of the tiled, so we need to write this:
        display_mouse = (mouse[0] * (display.get_width() / width), mouse[1] * (display.get_height() / height))

        clock.tick(fps)

        # displaying my background
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft)

        # displaying the player but we cant move it
        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft)

        # drawing the buttons
        shop_button = draw_button(display, 212.5, 227.5, 50, 22, "shop", text_color=brick_color,
                                  image_path="images/buttons/basic_button.png", font=cutefont)
        quit_shop_button = draw_button(display, 277.5, 227.5, 50, 22, "exit", text_color=brick_color,
                                       image_path="images/buttons/basic_button.png", font=cutefont)

        # Writing the welcome message to the shop
        draw_button(display, 187.5, 175, 150, 40, "welcome to the shop!", brick_color,
                    "images/dialogs/dialog box big.png", font=cutefont)

        # allowing the user to quit even tho they shouldn't because our game is perfect
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                progress()
                exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.collidepoint(display_mouse):
                    shop_menu(player)

                elif quit_shop_button.collidepoint(display_mouse):
                    player.just_left_store = True
                    return "main"

        # scaling and drawing the screen to the surface
        store_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        pygame.display.flip()


def shop_menu(player):
    """
    Handles the logic between the player interaction with the store menu.
    The player buys items inside of this function, which will then be added to their inventory.
    Also handles an event loop which when the mouse hovers over it, returns the description of the objects.

    Parameters
    ----------
    player: Player

    """
    shopping = True
    # creating my player group, so I can add my dog to it later:
    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    ################ TESTING THE TILES ###################
    store_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2, height // 2))

    ############################### CAVE MAP ################################

    tmx_data_store = load_pygame("data/WE STORE/WE STORE MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data_store, None, None, None, None)

    while shopping:
        mouse_pos = pygame.mouse.get_pos()

        # displaying my tiles background
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft)

        # scaling and drawing the screen to the surface
        store_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # drawing the actual store menu
        store_screen.blit(menu_store, (width // 2 - 375, height // 2 - 300))

        # setting up so my gold amount shows on store menu
        gold_available = inventoryfont.render(f"My Gold: {info['gold']}", True, brick_color)
        store_screen.blit(gold_available, (width // 2 - 310, height // 2 - 220))

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            # letting my player quit the game:
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # QUIT BUTTON
                if 946 <= mouse_pos[0] <= 987 and 110 <= mouse_pos[1] <= 152:
                    shopping = False
                # APPLE BUTTON
                if 348 <= mouse_pos[0] <= 445 and 291 <= mouse_pos[1] <= 334:
                    player.buy_item('apple')
                # MUSHROOM BUTTON
                if 509 <= mouse_pos[0] <= 605 and 291 <= mouse_pos[1] <= 334:
                    player.buy_item('mushroom')
                # POTION BUTTON
                if 670 <= mouse_pos[0] <= 766 and 291 <= mouse_pos[1] <= 334:
                    if player.inventory['speed potion'] == 1:
                        text = pygame.transform.scale(font_for_message.render("Can only have 1!", True, brick_color),
                                                      (500, 60))
                        screen.blit(text, (400, 300))
                        pygame.display.update()
                        pygame.time.wait(700)
                    else:
                        player.buy_item('speed potion')
                # SWORD BUTTON
                if 834 <= mouse_pos[0] <= 930 and 291 <= mouse_pos[1] <= 334:
                    player.buy_item('dagger')
                # LAST ROW
                # DOG BUTTON
                if 347 <= mouse_pos[0] <= 444 and 503 <= mouse_pos[1] <= 546:
                    # allowing the player to only have one dog
                    if player.inventory['dog'] == 1:
                        text = pygame.transform.scale(font_for_message.render("Can only have 1!", True, brick_color),
                                                      (500, 60))
                        screen.blit(text, (400, 300))
                        pygame.display.update()
                        pygame.time.wait(700)
                    else:
                        player.buy_item('dog')
                        if info['gold'] >= player.price_items['dog']:
                            dog_bark.play()
                            if not player.dog.bought:
                                player.dog.bought = True
                                info['inventory']['dog'] = 1
                                player_group.add(player.dog)

                # SOUP BUTTON
                if 499 <= mouse_pos[0] <= 600 and 503 <= mouse_pos[1] <= 546:
                    player.buy_item('soup')
                # BOW BUTTON
                if 673 <= mouse_pos[0] <= 767 and 503 <= mouse_pos[1] <= 546:
                    player.buy_item('ghost_bow')
                # KEY BUTTON
                if 832 <= mouse_pos[0] <= 926 and 500 <= mouse_pos[1] <= 543:
                    player.buy_item('key')

        for button in button_data.values():
            show_hover_message(screen, mouse_pos, button["rect"], button["description"])

        pygame.display.update()
