from config import *
from pytmx.util_pygame import load_pygame

from inventory import inventory_menu, scaled_images_inventory
from mouse_position import draw_button, get_scaled_mouse_position
from utils import area_setup, calculate_camera_offset, paused
from weapon import weapons

def shed_area(player):
    """
    A shed area where the player can upgrade their weapons.

    Parameters
    ----------
    player: Player
        The player object to control within the shed area.

    Returns
    -------
    str
        returns 'main' when the player leaves the shed

    """
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
        scaled_mouse_pos = get_scaled_mouse_position()
        # controlling the frame rate
        frame_time = clock.tick(fps)

        # Calculate camera offset
        camera_offset = calculate_camera_offset(player, display)

        # draw the tiles
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        inventory_button = draw_button(display, 500, y=10, width=70, height=35,
                                       text="Inventory",
                                       text_color=brick_color, image_path="images/buttons/basic_button.png",
                                       font=cutefont)

        # handling events:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if keys[pygame.K_SPACE]:
                paused()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inventory_menu(player)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory_button.collidepoint(scaled_mouse_pos):
                    inventory_menu(player)

        # updating the player group
        player_group.update(collision_sprites, display, frame_time)

        if exit_rect and exit_rect.colliderect(player.rect):
            player.just_left_shed = True
            return "main"

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        if work_table_rect and work_table_rect.colliderect(player.rect):
            crafting(player)

        shed_screen.blit(pygame.transform.scale(display, resolution), (0, 0))

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()

def crafting(player):
    """
    This function handles the crafting of weapons in the game.

    Parameters
    ----------
    player: pygame.sprite.Sprite
        The player sprite involved in the crafting process.

    """
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

    message = "Click on the stones to select a weapon and a crystal"
    message_text_to_display = font_for_message.render(message, True, white)

    platform_image = pygame.image.load("images/shed buttons/high_plat_rect-removebg-preview2.png").convert_alpha()
    evolve_image = pygame.image.load("images/shed buttons/Evolve-removebg-preview.png").convert_alpha()

    # resizing the images
    scaled_platform_image = pygame.transform.scale(platform_image, (115, 120))
    scaled_platform_image_2 = pygame.transform.scale(platform_image, (115, 120))
    scaled_evolve_image = pygame.transform.scale(evolve_image, (160, 50))

    # get their rectangles
    text_rect = message_text_to_display.get_rect(topleft=(100, 60))
    text_surface = pygame.Surface(text_rect.size, pygame.SRCALPHA)
    text_surface.fill((0, 0, 0, 0))  # transparent background
    text_surface.blit(font_for_message.render(message, True, white), (0, 0))

    platform_rect = scaled_platform_image.get_rect(topleft=(130, 75))
    platform_rect_2 = scaled_platform_image_2.get_rect(topleft=(320, 75))

    evolve_rect = scaled_evolve_image.get_rect(topleft=(205, 200))
    evolve_text = font_for_message.render("Evolve Weapon", True, yellow_torrado)
    evolve_text_rect = evolve_text.get_rect(center=evolve_rect.center)
    evolve_text_rect.y += 3

    chosen_weapon, chosen_crystal = None, None
    chosen_weapon_image, chosen_crystal_image = None, None

    error_message = None
    error_display_start = None
    error_display_duration = 0

    still_crafting = True
    while still_crafting:
        scaled_mouse_pos = get_scaled_mouse_position()
        frame_time = clock.tick(fps)

        # Calculate camera offset
        camera_offset = calculate_camera_offset(player, display)

        # draw the tiles
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        inventory_button = draw_button(display, 500, y=10, width=70, height=35,
                                       text="Inventory",
                                       text_color=brick_color, image_path="images/buttons/basic_button.png",
                                       font=cutefont)
        back_button = draw_button(display, 500, y=270, width=70, height=35,
                                  text="Back",
                                  text_color=brick_color, image_path="images/store/store_button.png",
                                  font=cutefont)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if keys[pygame.K_SPACE]:
                paused()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inventory_menu(player)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory_button.collidepoint(scaled_mouse_pos):
                    inventory_menu(player)
                if back_button.collidepoint(scaled_mouse_pos):
                    # this should be enough for the player to stop colliding with the work_table_rect
                    player.rect.centery += 10
                    progress()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle crafting selections
                if platform_rect.collidepoint(scaled_mouse_pos):
                    chosen_weapon = inventory_menu(player, place="shed", item_type="weapons")
                    if chosen_weapon:
                        chosen_weapon_image = scaled_images_inventory[chosen_weapon]
                elif platform_rect_2.collidepoint(scaled_mouse_pos):
                    chosen_crystal = inventory_menu(player, place="shed", item_type="crystals")
                    if chosen_crystal:
                        chosen_crystal_image = scaled_images_inventory[chosen_crystal]

                if evolve_rect.collidepoint(scaled_mouse_pos) and chosen_weapon and chosen_crystal:
                    # print("Evolve clicked!")
                    # evolve_weapon(player, display, chosen_weapon, chosen_crystal)
                    error_message, error_display_duration = evolve_weapon(player, chosen_weapon,
                                                                          chosen_crystal)
                    if error_message:
                        error_display_start = pygame.time.get_ticks()

        player_group.update(collision_sprites, display, frame_time)
        display.blit(text_surface, text_rect.topleft)
        display.blit(scaled_platform_image, platform_rect)
        display.blit(scaled_platform_image_2, platform_rect_2)
        display.blit(scaled_evolve_image, evolve_rect)

        display.blit(evolve_text, evolve_text_rect.topleft)

        # Display the chosen weapon on platform 1
        if chosen_weapon_image:
            weapon_pos = (platform_rect.centerx - chosen_weapon_image.get_width() // 2, platform_rect.centery -
                          chosen_weapon_image.get_height() // 2)
            display.blit(chosen_weapon_image.convert_alpha(), weapon_pos)

        # Display the chosen crystal on platform 2
        if chosen_crystal_image:
            crystal_pos = (platform_rect_2.centerx - chosen_crystal_image.get_width() // 2, platform_rect_2.centery -
                           chosen_crystal_image.get_height() // 2)
            display.blit(chosen_crystal_image.convert_alpha(), crystal_pos)

        if error_message and pygame.time.get_ticks() - error_display_start < error_display_duration * 1000:
            error_text_to_display = font_for_message.render(error_message, True, red)
            display.blit(error_text_to_display, (110, 300))
        elif error_message:  # Reset message after duration
            error_message = None

        shed_screen.blit(pygame.transform.scale(display, resolution), (0, 0))
        pygame.display.flip()

    progress()
    pygame.quit()
    exit()

def evolve_weapon(player, weapon, crystal):
    """
    Evolves the player's weapon based on the provided weapon and crystal combination.

    Parameters
    ----------
    player : pygame.sprite.Sprite
        The player sprite whose weapon is to be evolved.
    weapon : str
        The weapon to be evolved.
    crystal : str
        The crystal used for evolving the weapon.

    Returns
    -------
    Tuple
        A tuple containing an error message, if combination invalid, and the display duration for the error message.

    """
    error_message = None
    display_duration = 4

    if weapon == "dagger" and crystal == "red_crystal":
        info["inventory"]["dagger"] -= 1
        info["inventory"]["red_crystal"] -= 1
        info["inventory"]["fire_sword"] += 1
        player.inventory = info["inventory"]
        sparkly_music.play()

    elif weapon == "dagger" and crystal == "blue_crystal":
        info["inventory"]["dagger"] -= 1
        info["inventory"]["blue_crystal"] -= 1
        info["inventory"]["winter_sword"] += 1
        player.inventory = info["inventory"]
        sparkly_music.play()

    elif weapon == "ghost_bow" and crystal == "white_crystal":
        info["inventory"]["ghost_bow"] -= 1
        info["inventory"]["white_crystal"] -= 1
        info["inventory"]["ice_bow"] += 1
        player.inventory = info["inventory"]
        sparkly_music.play()

    elif weapon == "ghost_bow" and crystal == "gold_crystal":
        info["inventory"]["ghost_bow"] -= 1
        info["inventory"]["gold_crystal"] -= 1
        info["inventory"]["light_bow"] += 1
        player.inventory = info["inventory"]
        sparkly_music.play()

    # damage increases 20% of damage for that weapon, and future one you might create (of the same type)
    elif any(element in weapon for element in ["sword", "bow", "axe", "dagger"]) and crystal == "purple_crystal":
        current_damage = info["weapon_attributes_evolved"][weapon]
        default_damage = weapons[weapon]["damage"]
        multiplications = current_damage / default_damage
        if multiplications <= 1.2 ** 4:  # 5 multiplications allowed
            info["inventory"]["purple_crystal"] -= 1
            info["weapon_attributes_evolved"][weapon] *= 1.2
            sparkly_music.play()
        else:
            error_message = "Weapon at max level"

    else:
        error_message = "Invalid combination of weapon and crystal"

    progress()
    return error_message, display_duration