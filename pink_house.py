from config import *
from pytmx.util_pygame import load_pygame
from utils import area_setup, calculate_camera_offset
from utils import paused
from mouse_position import draw_button

def pink_house_area(player):
    """
    Handles the game logic inside the abandoned house area.
    The player can find a chest and earn money.

    Parameters
    ----------
    player: Player

    Returns
    ----------
    str
        returns 'main' when player leaves the abandoned house

    """
    clock = pygame.time.Clock()
    home_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### HOUSE MAP ################################

    tmx_data = load_pygame("data/WE PINK HOUSE/WE PINK HOUSE MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data, "collisions",
                                                                                "exit house",
                                                                                "prize", None)

    ####################################################################

    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (580, 450)
    player.state = "down"
    ###################################### MAIN GAME LOOP #######################################
    running = True

    while running:
        # controlling the frame rate
        frame_time = clock.tick(fps)

        # handling events:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if keys[pygame.K_SPACE]:
                paused()

        # Calculate camera offset
        camera_offset = calculate_camera_offset(player, display)

        # draw the tiles
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group
        player_group.update(collision_sprites, display, frame_time)

        if exit_rect and exit_rect.colliderect(player.rect):
            player.just_left_pink_house = True
            return "main"

        if clues_rect and clues_rect.colliderect(player.rect):
            if info['abandoned_chest'] <= 0:
                draw_button(display, 10, 150, 320, 100,
                            "click  'E'  to  claim  abandoned  gold!", brick_color,
                            "images/inventory/inventory_menu.png", cutefont)
                display.blit(gold_chest, (150, 150))
                if keys[pygame.K_e]:
                    coin_music.play()
                    info['abandoned_chest'] = 1
                    player.add_gold(150)
                    # this way the player can only open this chest once in the whole game
            else:
                draw_button(display, 10, 150, 320, 100,
                            "+ 50  gold   (already  claimed)", brick_color,
                            "images/inventory/inventory_menu.png", cutefont)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        home_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()