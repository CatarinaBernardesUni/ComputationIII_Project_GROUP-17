from player import Player
from mouse_position import get_mouse_position, draw_button
import pygame
from pytmx.util_pygame import load_pygame
from tile import Tile
from config import *
from pytmx.util_pygame import load_pygame
from tile import Tile
from mouse_position import button_data, show_hover_message

<<<<<<< HEAD
=======

>>>>>>> e069fa211a1d34dd4aae015314129dfc796fa584
def store_setup(tmx_data_store):
    background_sprite_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    objects_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
<<<<<<< HEAD
    cave_exit_rect = None
=======
>>>>>>> e069fa211a1d34dd4aae015314129dfc796fa584

    # static tiles
    for layer in tmx_data_store.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(position=pos, surf=surface, groups=(background_sprite_group, tiles_group))

<<<<<<< HEAD

    return (background_sprite_group, tiles_group, objects_group,
            collision_sprites, cave_exit_rect)
=======
    return background_sprite_group, tiles_group, objects_group, collision_sprites
>>>>>>> e069fa211a1d34dd4aae015314129dfc796fa584


def inside_store(player):

    # setting up a background
    store_owner = pygame.image.load("images/store/store_owner.png")
    store_owner = pygame.transform.scale(store_owner, (100, 100))
    store_owner_position = (600, 400)

<<<<<<< HEAD

=======
>>>>>>> e069fa211a1d34dd4aae015314129dfc796fa584
    ################ TESTING THE TILES ###################
    store_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### STORE MAP ################################

<<<<<<< HEAD

    tmx_data_cave = load_pygame("data/WE STORE/")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, cave_exit_rect) = cave_setup(tmx_data_cave)
=======
    tmx_data_store = load_pygame("data/WE STORE/WE STORE MAP.tmx")
    background_sprite_group, tiles_group, objects_group, collision_sprites = store_setup(tmx_data_store)

>>>>>>> e069fa211a1d34dd4aae015314129dfc796fa584
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
                progress()
                exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.collidepoint(mouse):
                    shop_menu(player)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if quit_shop_button.collidepoint(mouse):
                    return

        # displaying my background
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft)

        # scalling and bliting the screen to the surface
        store_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # displaying the store owner
        screen.blit(store_owner, store_owner_position)

        # drawing the buttons
        shop_button = draw_button(screen, 255, 335, 190, 65, "shop", text_color=deep_black, image_path="images/store/store_button.png", font=cutefont)
        quit_shop_button = draw_button(screen, 475, 335, 245, 65, "leave shop", text_color=deep_black, image_path="images/store/store_button.png", font=cutefont)
        draw_button(screen, 255, 190, 450, 120, "welcome to the shop!", deep_black, "images/store/board.png", font=cutefont)

        # updating the display
        pygame.display.update()


def shop_menu(player):
    shopping = True
    custom_font = pygame.font.Font("fonts/Minecraft.ttf", 20)

    ################ TESTING THE TILES ###################
    store_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### CAVE MAP ################################

    tmx_data_store = load_pygame("data/WE STORE/WE STORE MAP.tmx")
    background_sprite_group, tiles_group, objects_group, collision_sprites = store_setup(tmx_data_store)


    while shopping:

        # displaying my tiles background
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft)

        # scaling and blitting the screen to the surface
        store_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # bliting the actual store menu
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