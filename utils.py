# import config
from collision import CollisionObject
import interface
from config import *
# from pytmx.util_pygame import load_pygame
from tile import Tile
from mouse_position import draw_button, get_mouse_position


def paused():
    pause = True
    while pause:
        screen.blit(pause_image, (0, 0))
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 443 <= mouse[0] <= 610 and 112 <= mouse[1] <= 169:
                    main_music.stop()
                    battle_music.stop()
                    menu_music.play(-1)
                    interface.interface()
                if 637 <= mouse[0] <= 802 and 112 <= mouse[1] <= 171:
                    pause = False
        pygame.display.update()


# letting all the sounds be updated throughout the game
def update_all_volumes(all_sounds, global_volume):
    """
    Updates all sounds in the list throughout the game.
    :param all_sounds: a list of all the sounds in the game
    :param global_volume: a global volume variable for all the sounds in the game.

    :return: None
    """
    for sound in all_sounds:
        sound.set_volume(global_volume)


# Function to draw the music bar
def music_bar(screen, bar_x, bar_y, bar_width, bar_height, global_volume):
    """
    This function draws a music volume bar with buttons to increase or decrease the volume.
    The slider is updated everytime the user clicks on a button, based on the global_volume and the bar itself.
    The function returns the minus and plus button so the volume is implemented later.

    :param screen: the screen where the music bar will be displayed
    :param bar_x: the x-coordinate of the music bar.
    :param bar_y: the y-coordinate of the music bar.
    :param bar_width: the width of the music bar.
    :param bar_height: the height of the music bar.
    :param global_volume: the current global volume level (from 0.0 to 1.0).

    :return: minus and plus button volume
    """
    # Draw the plus and minus buttons
    minus_button = draw_button(screen, bar_x - 100 - 10, bar_y + (bar_height - 90) // 2, 100, 90, 'MINUS', brick_color,
                               'images/store/store_button.png', settingsfont)
    plus_button = draw_button(screen, bar_x + bar_width + 10, bar_y + (bar_height - 90) // 2, 100, 90, 'PLUS',
                              brick_color, 'images/store/store_button.png', settingsfont)

    # Draw the main bar
    pygame.draw.rect(screen, brick_color, (bar_x, bar_y, bar_width, bar_height))

    # Draw the slider
    slider_x = bar_x + (global_volume * bar_width) - (bar_height // 2)
    pygame.draw.rect(screen, white, (slider_x, bar_y - (bar_height // 2), bar_height, bar_height * 2))

    return minus_button, plus_button


def options_menu():

    """
    This function creates an option menu where the user will be able to adjust the volume of the game.

    The music bar is implemented in this screen. If the user hits the minus button, teh global_volume
    is decreased by 0.1, or vice versa if hit the plus button.
    Then, the music_bar() function is updated and all the music throughout the game is updated through the
    update_all_sounds() function.

    :return: None
    """
    global global_volume
    # Set up the display
    screen = pygame.display.set_mode(resolution)

    # setting a background
    options_background = pygame.image.load("images/options/options_trial.png")

    # size of the music bar
    bar_width = 400
    bar_height = 20
    bar_x = (resolution[0] - bar_width) // 2
    bar_y = (resolution[1] - bar_height) // 2

    running = True
    while running:
        # getting the mouse position
        mouse = get_mouse_position()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Draw the music bar and its most recent value
                minus_button, plus_button = music_bar(screen, bar_x, bar_y, bar_width, bar_height, global_volume)
                # minus sign is clicked
                if minus_button.collidepoint(mouse):
                    global_volume = max(0, global_volume - 0.1)
                    update_all_volumes(all_sounds, global_volume)
                # plus sign is clicked
                elif plus_button.collidepoint(mouse):
                    global_volume = min(1, global_volume + 0.1)
                    update_all_volumes(all_sounds, global_volume)
                # quit button:
                if quit_options_button.collidepoint(mouse):
                    progress()
                    return

        # Display the background
        screen.blit(options_background, (0, 0))

        # display the music bar on the screen:
        music_bar(screen, bar_x, bar_y, bar_width, bar_height, global_volume)

        # Display the volume percentage
        volume_percentage = int(global_volume * 100)
        volume_text = settingsfont.render(f"Volume: {volume_percentage}%", False, white)
        volume_text_rect = volume_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height + 50))
        screen.blit(volume_text, volume_text_rect)

        # drawing the quit button to leave the options menu
        quit_options_button = draw_button(screen, 1000, 520, 150, 80, "EXIT", text_color=brick_color,
                                          image_path="images/store/store_button.png", font=settingsfont)

        # Update the display
        pygame.display.flip()
        progress()


def area_setup(tmx_data, collisions_name, exit_name, clues_name, someone_talks):
    """
    Sets up the area by loading tiles, objects and collision data from the TMX data.
    This function helps to implement the interior of the houses and other TMX related data.

    :param tmx_data: TMX data containing the map information.
    :param collisions_name: the name of the layer containing the collisions objects.
    :param exit_name: the name of the layer containing the exit object.
    :param clues_name: the name of the layer containing the clue object.
    :param someone_talks: the name of the layer containing objects that trigger speech bubbles.

    :return: Returns a tuple containing the background sprite group, tiles group, objects group,
        collision sprites group, exit rectangle, speech bubble rectangle, and clues rectangle.
    """

    background_sprite_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    objects_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    exit_rect = None
    speech_bubble_rect = None
    clues_rect = None

    for layer in tmx_data.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(position=pos, surf=surface, groups=(background_sprite_group, tiles_group))

    for obj in tmx_data.objects:
        if obj.image:  # no rectangles are entering here because they do not have images
            scaled_image = pygame.transform.scale(obj.image, (obj.width, obj.height))
            pos = (obj.x, obj.y)
            Tile(position=pos, surf=scaled_image, groups=(background_sprite_group, objects_group))
        if collisions_name:
            if obj in tmx_data.get_layer_by_name(collisions_name):
                CollisionObject(position=(obj.x, obj.y), size=(obj.width, obj.height), groups=(background_sprite_group,
                                                                                               collision_sprites))
        if exit_name:
            if obj in tmx_data.get_layer_by_name(exit_name):
                exit_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        # this checks if there's any clues or if it's set to None
        if clues_name:
            if obj in tmx_data.get_layer_by_name(clues_name):
                clues_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        # checks if someone talks or if it's None (this is for the old lady and cave)
        if someone_talks:
            if obj in tmx_data.get_layer_by_name(someone_talks):
                speech_bubble_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    return (background_sprite_group, tiles_group, objects_group,
            collision_sprites, exit_rect, speech_bubble_rect, clues_rect)


def calculate_camera_offset(player, display):
    """
    Calculates the camera offset to center the player on the screen while placing the
    camera within the map boundaries.

    :param player: The player object containing the player's position and rectangle.
    :param display: The display surface to render the game.
    :return: An object representing the camera offset.
    """

    camera_x = player.rect.centerx - display.get_width() // 2
    camera_y = player.rect.centery - display.get_height() // 2

    # Clamp the camera within the map boundaries
    camera_x = max(0, min(camera_x, width - display.get_width()))
    camera_y = max(0, min(camera_y, height - display.get_height()))

    camera_offset = pygame.Vector2(-camera_x, -camera_y)
    return camera_offset


def credits_():
    """
    Displays the credits screen and handles to return to the main menu.

    :return: previous screen
    """

    # Set up the display
    screen = pygame.display.set_mode(resolution)

    # main background for credits
    credits_background = pygame.image.load("images/credits/CREDITS.png")

    # main loop to detect user input and display the credits
    while True:
        # getting the position of the users mouse
        mouse = get_mouse_position()

        for ev in pygame.event.get():
            # allow the user to quit on (x)
            if ev.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            # creating a button that returns to main menu
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if quit_options_button.collidepoint(mouse):
                    return

        # Display the background
        screen.blit(credits_background, (0, 0))

        # drawing the quit button to leave the options menu
        quit_options_button = draw_button(screen, 1065, 555, 150, 80, "EXIT", text_color=brick_color,
                                          image_path="images/store/store_button.png", font=settingsfont)

        # Update the display
        pygame.display.flip()


def reset_progress():
    """
    Resets the player's progress by setting default values for health, gold, inventory, and other game attributes.

    :return: None
    """
    info['health'] = 5
    info['gold'] = 50
    info['inventory'] = {key: 0 for key in info['inventory']}
    info["claimed_chest_home"], info["stolen_grandma"], info['abandoned_chest'] = 0, 0, 0
    info['current_wave'] = 1
    info["weapon_attributes_evolved"]["dagger"] = 18
    info["weapon_attributes_evolved"]["ghost_bow"] = 22
    info["weapon_attributes_evolved"]["winter_sword"] = 18
    info["weapon_attributes_evolved"]["gold_axe"] = 22
    info["weapon_attributes_evolved"]["fire_sword"] = 28
    info["weapon_attributes_evolved"]["ice_bow"] = 24
    info["weapon_attributes_evolved"]["light_bow"] = 23
    info["weapon_attributes_evolved"]["ruby_axe"] = 15
