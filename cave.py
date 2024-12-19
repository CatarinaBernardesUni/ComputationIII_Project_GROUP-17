from config import *
from pytmx.util_pygame import load_pygame

from mouse_position import draw_button
# from game import paused
from utils import area_setup, paused, calculate_camera_offset


def cave_area(player):
    clock = pygame.time.Clock()
    cave_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### CAVE MAP ################################

    tmx_data = load_pygame("data/WE CAVE/WE CAVE.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data, "collisions on cave",
                                                                                "cave exit", None, "speech")
    # doing this outside the area setup function because it is a specific thing from the cave
    spike_rects = []
    purple_crystal_rect = None
    red_crystal_rect = None
    gold_crystal_rect = None
    white_crystal_rect = None
    blue_crystal_rect = None

    for obj in tmx_data.objects:
        if obj in tmx_data.get_layer_by_name("spike rect"):
            # there are several spike rects
            spike_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            spike_rects.append(spike_rect)

        if obj in tmx_data.get_layer_by_name("purple crystal"):
            purple_crystal_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        if obj in tmx_data.get_layer_by_name("red crystal"):
            red_crystal_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        if obj in tmx_data.get_layer_by_name("gold crystal"):
            gold_crystal_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        if obj in tmx_data.get_layer_by_name("white crystal"):
            white_crystal_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        if obj in tmx_data.get_layer_by_name("blue crystal"):
            blue_crystal_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    ####################################################################

    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # setting the player initial position on the cave
    player.rect.center = (670, 320)
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
        # tiles_group.draw(display)
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group
        player_group.update(collision_sprites, display, frame_time, spike_rects=spike_rects)

        if exit_rect and exit_rect.colliderect(player.rect):
            player.just_left_cave = True
            return "main"

        if speech_bubble_rect and speech_bubble_rect.colliderect(player.rect):
            draw_button(display, 130, 80, 150, 100,
                        "Did we fix it?", brick_color,
                        "images/dialogs/dialog box medium mirrored.png", cutefont)
            draw_button(display, 365, 60, 150, 100,
                        "Yes, we did!!!", brick_color,
                        "images/dialogs/dialog box medium.png", cutefont)

        # using if and elif for the buttons not to appear above each other
        if purple_crystal_rect and purple_crystal_rect.colliderect(player.rect):
            draw_button(display, 20, 110, 250, 50,
                        "Click  'E'  to  collect a purple crystal!", brick_color,
                        "images/dialogs/dialog box medium mirrored.png", cutefont)
            if keys[pygame.K_e]:
                pass

        elif red_crystal_rect and red_crystal_rect.colliderect(player.rect):
            draw_button(display, 80, 110, 250, 50,
                        "Click  'E'  to  collect a red crystal!", brick_color,
                        "images/dialogs/dialog box medium mirrored.png", cutefont)
            if keys[pygame.K_e]:
                pass

        elif gold_crystal_rect and gold_crystal_rect.colliderect(player.rect):
            draw_button(display, 20, 150, 250, 50,
                        "Click  'E'  to  collect a gold crystal!", brick_color,
                        "images/dialogs/dialog box medium mirrored.png", cutefont)
            if keys[pygame.K_e]:
                pass

        elif blue_crystal_rect and blue_crystal_rect.colliderect(player.rect):
            draw_button(display, 290, 110, 250, 50,
                        "Click  'E'  to  collect a blue crystal!", brick_color,
                        "images/dialogs/dialog box medium.png", cutefont)
            if keys[pygame.K_e]:
                pass

        elif white_crystal_rect and white_crystal_rect.colliderect(player.rect):
            draw_button(display, 20, 110, 250, 50,
                        "Click  'E'  to  collect a white crystal!", brick_color,
                        "images/dialogs/dialog box medium mirrored.png", cutefont)
            if keys[pygame.K_e]:
                pass

        # display.blit(player_score_surf, player_score_rect)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        cave_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()
