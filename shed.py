from config import *
from pytmx.util_pygame import load_pygame

from inventory import inventory_menu
from utils import area_setup, calculate_camera_offset, paused

def shed_area(player):
    clock = pygame.time.Clock()
    shed_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### HOUSE MAP ################################

    tmx_data = load_pygame("data/WE SHED/WE SHED.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, work_table_rect, clues_rect) = area_setup(tmx_data, "Collisions",
                                                                             "exit", None,
                                                                             "Work table")

    ####################################################################
    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (530, 460)
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
            player.just_left_shed = True
            return "main"

        if work_table_rect and work_table_rect.colliderect(player.rect):
            crafting(player)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        shed_screen.blit(pygame.transform.scale(display, resolution), (0, 0))

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()

def crafting(player):
    font_for_message = pygame.font.Font("fonts/pixel_font.ttf", 32)
    message = "Open your inventory and select one weapon and a crystal"

    platform_image = pygame.image.load("images/shed buttons/rect_plat.png")
    evolve_image = pygame.image.load("images/shed buttons/Evolve-removebg-preview.png")

    # redimentioning the images
    scaled_platform_image = pygame.transform.scale(platform_image, (230, 240))
    scaled_platform_image_2 = pygame.transform.scale(platform_image, (230, 240))
    scaled_evolve_image = pygame.transform.scale(evolve_image, (320, 100))

    # get their rectangles
    platform_rect = scaled_platform_image.get_rect(topleft=(340, 150))
    platform_rect_2 = scaled_platform_image_2.get_rect(topleft=(700, 150))
    evolve_rect = scaled_evolve_image.get_rect(topleft=(490, 400))

    still_crafting = True
    while still_crafting:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if platform_rect.collidepoint(mouse_pos):
                    print("Platform 1 clicked!")
                    chosen_weapon = inventory_menu(player, place="shed", item_type="weapons")
                    # todo: display the selected item and close the inventory

                if platform_rect_2.collidepoint(mouse_pos):
                    print("Platform 2 clicked!")
                    chosen_crystal = inventory_menu(player, place="shed", item_type="crystals")

        screen.blit(scaled_platform_image, platform_rect)
        screen.blit(scaled_platform_image_2, platform_rect_2)
        screen.blit(scaled_evolve_image, evolve_rect)

        evolve_rect_text = font_for_message.render("Evolve Weapon", True, yellow_torrado)
        screen.blit(evolve_rect_text, (evolve_rect.centerx - 114, evolve_rect.centery - 10))

        pygame.display.update()

    progress()
    pygame.quit()
    exit()