from config import *
from pytmx.util_pygame import load_pygame

from inventory import inventory_menu, scaled_images_inventory
from utils import area_setup, calculate_camera_offset, paused

def shed_area(player):
    clock = pygame.time.Clock()
    shed_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### SHED MAP ################################

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
    ###################################### MAIN SHED LOOP #######################################
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

    chosen_weapon = None
    chosen_weapon_image = None
    chosen_crystal = None
    chosen_crystal_image = None

    message = "Click on the stones to select a weapon and a crystal"
    message_text_to_display = font_for_message.render(message, True, white)

    platform_image = pygame.image.load("images/shed buttons/rect_plat.png")
    evolve_image = pygame.image.load("images/shed buttons/Evolve-removebg-preview.png")

    # resizing the images
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
                progress()
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if platform_rect.collidepoint(mouse_pos):
                    print("Platform 1 clicked!")
                    chosen_weapon = inventory_menu(player, place="shed", item_type="weapons")
                    # using an if to check if the image exists before, or it will give an error if
                    # we click on an empty space in the inventory
                    if chosen_weapon:
                        original_image = scaled_images_inventory[chosen_weapon]
                        # resizing the image to look better on the platform
                        chosen_weapon_image = pygame.transform.scale(
                            original_image, (original_image.get_width() * 1.9, original_image.get_height() * 1.9))

                if platform_rect_2.collidepoint(mouse_pos):
                    print("Platform 2 clicked!")
                    chosen_crystal = inventory_menu(player, place="shed", item_type="crystals")
                    if chosen_crystal:
                        original_image = scaled_images_inventory[chosen_crystal]
                        # resizing the image to look better on the platform
                        chosen_crystal_image = pygame.transform.scale(
                            original_image, (original_image.get_width() * 2, original_image.get_height() * 2))

                if evolve_rect.collidepoint(mouse_pos) and chosen_weapon and chosen_crystal:
                    print("Evolve clicked!")
                    evolve_weapon(player, chosen_weapon, chosen_crystal)

        screen.blit(message_text_to_display, (150, 120))
        screen.blit(scaled_platform_image, platform_rect)
        screen.blit(scaled_platform_image_2, platform_rect_2)
        screen.blit(scaled_evolve_image, evolve_rect)

        evolve_rect_text = font_for_message.render("Evolve Weapon", True, yellow_torrado)
        screen.blit(evolve_rect_text, (evolve_rect.centerx - 114, evolve_rect.centery - 10))

        # Display the chosen weapon on platform 1
        if chosen_weapon_image:
            weapon_pos = (platform_rect.centerx - chosen_weapon_image.get_width() // 2, platform_rect.centery -
                          chosen_weapon_image.get_height() // 2)
            screen.blit(chosen_weapon_image, weapon_pos)

        # Display the chosen crystal on platform 2
        if chosen_crystal_image:
            crystal_pos = (platform_rect_2.centerx - chosen_crystal_image.get_width() // 2, platform_rect_2.centery -
                           chosen_crystal_image.get_height() // 2)
            screen.blit(chosen_crystal_image, crystal_pos)

        pygame.display.flip()

    progress()
    pygame.quit()
    exit()

def evolve_weapon(player, weapon, crystal):
    if weapon == "dagger" and crystal == "red_crystal":
        info["inventory"]["dagger"] -= 1
        info["inventory"]["red_crystal"] -= 1
        info["inventory"]["fire_sword"] += 1
        player.inventory = info["inventory"]

    elif weapon == "dagger" and crystal == "blue_crystal":
        info["inventory"]["dagger"] -= 1
        info["inventory"]["blue_crystal"] -= 1
        info["inventory"]["ice_sword"] += 1
        player.inventory = info["inventory"]

    elif weapon == "ghost_bow" and crystal == "white_crystal":
        info["inventory"]["ghost_bow"] -= 1
        info["inventory"]["white_crystal"] -= 1
        info["inventory"]["ice_bow"] += 1
        player.inventory = info["inventory"]

    elif weapon == "ghost_bow" and crystal == "gold_crystal":
        info["inventory"]["ghost_bow"] -= 1
        info["inventory"]["gold_crystal"] -= 1
        info["inventory"]["light_bow"] += 1
        player.inventory = info["inventory"]

    # damage increases 20% for that instance of the weapon, not future ones
    # if you spend your weapon by evolving it to another, the player looses its upgrades
    elif weapon in player.weapons.keys() and crystal == "purple_crystal":
        info["inventory"]["purple_crystal"] -= 1
        # getting the class of the weapon that the player is evolving
        # weapon_class = player.weapons[weapon].__class__
        # updating all future instances of the weapon
        # player.weapons[weapon] = weapon_class(player, player.active_weapon_group, weapon).upgrade()

    else:
        error_message = "Invalid combination of weapon and crystal or weapon at max level"
        error_text_to_display = font_for_message.render(error_message, True, red)
        screen.blit(error_text_to_display, (130, 520))

    progress()