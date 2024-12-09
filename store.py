from player import Player
from mouse_position import get_mouse_position, draw_button
import pygame
from config import *
from pytmx.util_pygame import load_pygame
from tile import Tile
from mouse_position import button_data, show_hover_message
from utils import area_setup

"""
def store_setup(tmx_data_store):
    background_sprite_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    objects_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()

    # static tiles
    for layer in tmx_data_store.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(position=pos, surf=surface, groups=(background_sprite_group, tiles_group))

    return background_sprite_group, tiles_group, objects_group, collision_sprites

"""


def inside_store(player):
    # setting up a background
    store_owner = pygame.image.load("images/store/store_owner.png")
    store_owner = pygame.transform.scale(store_owner, (40, 40))
    store_owner_position = (320, 225)

    ################ TESTING THE TILES ###################
    store_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2, height // 2))
    print(display)
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

    # setting the player initial position on the cave
    player.rect.center = (300, 320)
    player.state = "up"

    # setting up fonts for the text
    cutefont = pygame.font.Font("fonts/Minecraft.ttf", 15)

    # creating an event loop
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        display_mouse = (mouse[0] * (display.get_width() / width), mouse[1] * (display.get_height() / height))

        clock.tick(fps)

        # displaying my background
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft)

        # displaying the store owner
        display.blit(store_owner, store_owner_position)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft)

        # drawing the buttons
        shop_button = draw_button(display, 177.5, 167.5, 95, 32.5, "shop", text_color=deep_black,
                                  image_path="images/store/store_button.png", font=cutefont)
        quit_shop_button = draw_button(display, 287.5, 167.5, 122.5, 32.5, "leave shop", text_color=deep_black,
                                       image_path="images/store/store_button.png", font=cutefont)
        draw_button(display, 177.5, 95, 225, 60, "welcome to the shop!", deep_black, "images/store/board.png",
                    font=cutefont)

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

        # scalling and bliting the screen to the surface
        store_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # updating the display
        pygame.display.flip()
        # player_group.update(collision_sprites, display)


def shop_menu(player):
    shopping = True
    custom_font = pygame.font.Font("fonts/Minecraft.ttf", 20)

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

        # scaling and blitting the screen to the surface
        store_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # bliting the actual store menu
        store_screen.blit(menu_store, (width // 2 - 375, height // 2 - 300))

        # setting up so my gold amount shows on store menu
        gold_available = custom_font.render(f"My Gold: {player.gold}", True, brick_color)
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
                    player.buy_item('speed potion')
                # SWORD BUTTON
                if 834 <= mouse_pos[0] <= 930 and 291 <= mouse_pos[1] <= 334:
                    player.buy_item('sword')
                # LAST ROW
                # DOG BUTTON
                if 347 <= mouse_pos[0] <= 444 and 503 <= mouse_pos[1] <= 546:
                    player.buy_item('dog')
                # SOUP BUTTON
                if 499 <= mouse_pos[0] <= 600 and 503 <= mouse_pos[1] <= 546:
                    player.buy_item('soup')
                # BOW BUTTON
                if 673 <= mouse_pos[0] <= 767 and 503 <= mouse_pos[1] <= 546:
                    player.buy_item('bow')
                # KEY BUTTON
                if 832 <= mouse_pos[0] <= 926 and 500 <= mouse_pos[1] <= 543:
                    player.buy_item('key')

        for button in button_data.values():
            show_hover_message(screen, mouse_pos, button["rect"], button["description"])

        pygame.display.update()
