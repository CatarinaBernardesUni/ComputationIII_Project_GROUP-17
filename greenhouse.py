from utils import *
from pytmx.util_pygame import load_pygame


def greenhouse_area(player):
    clock = pygame.time.Clock()
    home_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    tmx_data = load_pygame("data/WE OLD LADY HOUSE/WE OLD LADY HOUSE MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data, "collisions", "exit", None,
                                                                                None)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (111, 253)
    player.state = "up"
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
        camera_offset = calculate_camera_offset(player, display)
        ####################################################################################

        # draw the tiles
        # tiles_group.draw(display)
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group
        player_group.update(collision_sprites, display, frame_time)

        if exit_rect and exit_rect.colliderect(player.rect):
            player.just_left_greenhouse = True
            return "main"

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        home_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left
        display.fill("black")

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()
        # clock.tick(fps)
    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()
