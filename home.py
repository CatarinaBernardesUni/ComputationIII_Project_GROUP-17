
from config import *
from pytmx.util_pygame import load_pygame
from utils import area_setup
from utils import paused
from mouse_position import draw_button


def home_area(player):
    clock = pygame.time.Clock()
    home_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### HOUSE MAP ################################

    tmx_data = load_pygame("data/WE HOME/WE HOME MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data, "collisions on home", "home "
                                                                                                                "exit",
                                                                                "clue", None)

    ####################################################################

    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (385, 550)
    player.state = "down"

    # check if the chest is collected
    chest_opened = False
    first_chest_show = False

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


        ############################### CAMERA - REPEATED CODE ################################
        # Calculate camera offset
        camera_x = player.rect.centerx - display.get_width() // 2
        camera_y = player.rect.centery - display.get_height() // 2

        # Clamp the camera within the map boundaries
        camera_x = max(0, min(camera_x, width - display.get_width()))
        camera_y = max(0, min(camera_y, height - display.get_height()))

        camera_offset = pygame.Vector2(-camera_x, -camera_y)
        ####################################################################################

        # draw the tiles
        # tiles_group.draw(display)
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group
        player_group.update(collision_sprites, display)

        if exit_rect and exit_rect.colliderect(player.rect):
            player.just_left_home = True
            return "main"

        if clues_rect and clues_rect.colliderect(player.rect):
            print(f"Chest opened: {chest_opened}, First message shown: {first_chest_show}")
            if not chest_opened and not first_chest_show:
                draw_button(display, 100, 200, 320, 100,
                            "100 gold gleams in your grasp, but beware its price.", brick_color,
                            "images/inventory/inventory_menu.png", cutefont)
                player.add_gold(100)
                chest_opened = True
                first_chest_show = True

            # if the player bumps into the chest again, it does not let it collect the prize again
            elif chest_opened:
                 # only show 2nd message when 1st was shown
                if not first_chest_show:
                    draw_button(display, 100, 200, 320, 100,
                                "The prize is already in your possession", brick_color,
                                "images/inventory/inventory_menu.png", cutefont)

        # resets the message state once the player moves away
        elif clues_rect and not clues_rect.colliderect(player.rect):
            print("Player moved away from chest.")
            if not clues_rect.colliderect(player.rect):
                first_chest_show = False


        # display.blit(player_score_surf, player_score_rect)

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
