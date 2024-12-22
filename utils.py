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
    for sound in all_sounds:
        sound.set_volume(global_volume)


# Function to draw the music bar
def music_bar(screen, bar_x, bar_y, bar_width, bar_height, global_volume):
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


# Function to draw a stick figure with a construction hat
def draw_stick_figure_with_hat(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg

    # hat
    hat_color = (255, 215, 0)

    # drawing the construction hat
    pygame.draw.rect(screen, hat_color, [x - 25, y - 30, 50, 10])  # Hat's brim
    pygame.draw.rect(screen, hat_color, [x - 20, y - 40, 40, 20])  # Hat's dome


# Function to draw a normal stick figure (without a hat)
def draw_normal_stick_figure(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg


def under_construction():
    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversation_font = pygame.font.SysFont("Arial", 30)

    # setting my texts:
    back_text = corbelfont.render("back", True, white)
    construction_text = corbelfont.render("UNDER CONSTRUCTION", True, white)
    first_speech = conversation_font.render("Can we fix it?", True, white)
    bob_speech = conversation_font.render("Probably not...", True, white)

    # setting up the "images" position
    bob_x_position = 460
    bob_y_position = 450

    normal_x_position = 260
    normal_y_position = 450

    # same old, same old... while True loop
    while True:
        # getting the mouse position
        mouse = pygame.mouse.get_pos()  # probably good idea to create a function to write this

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    return  # return from where it was before

        # displaying the screen:
        screen.fill(deep_black)

        # displaying the main UNDER CONSTRUCTION TEXT
        construction_rect = construction_text.get_rect(center=(720 // 2, 300))
        screen.blit(construction_text, construction_rect)

        # drawing the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # stick figures text and "images"
        draw_normal_stick_figure(screen, normal_x_position, normal_y_position)
        draw_stick_figure_with_hat(screen, bob_x_position, bob_y_position)

        screen.blit(first_speech, (normal_x_position - 60, normal_y_position - 80))
        screen.blit(bob_speech, (bob_x_position - 60, bob_y_position - 80))

        # finally, as always, updating our screen
        pygame.display.update()


def area_setup(tmx_data, collisions_name, exit_name, clues_name, someone_talks):
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
    camera_x = player.rect.centerx - display.get_width() // 2
    camera_y = player.rect.centery - display.get_height() // 2

    # Clamp the camera within the map boundaries
    camera_x = max(0, min(camera_x, width - display.get_width()))
    camera_y = max(0, min(camera_y, height - display.get_height()))

    camera_offset = pygame.Vector2(-camera_x, -camera_y)
    return camera_offset


def credits_():
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
