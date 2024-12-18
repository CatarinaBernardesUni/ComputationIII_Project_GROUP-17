# Config file used to set global variables and other settings
# COLORS AND PICTURES HERE FOR NOW
from progress import *
from mouse_position import draw_button

# COLORS
dark_red = (138, 0, 0)  # Dark red for buttons
deep_black = (19, 20, 20)  # Almost black for background
grey = (59, 60, 60)  # Dark grey for alternate buttons
white = (254, 255, 255)  # White for readable text
glowing_light_red = (239, 128, 128)  # Light red for brighter text
blue = (207, 113, 209)
green = (137, 168, 38)
yellow = (255, 255, 0)
red = (150, 0, 24)
cute_purple = (128, 0, 128)
greenish = (182, 215, 168)

brick_color_transparent = (117, 49, 40, 225)
brick_color = (117, 49, 40)

# global volume for all music
global_volume = 0.5


# hearts
full_heart = pygame.transform.scale(pygame.image.load("images/others/full_heart.png"), (33, 33))
empty_heart = pygame.transform.scale(pygame.image.load("images/others/empty_heart.png"), (33, 33))


# font for the game
cutefont = pygame.font.Font("fonts/pixel_font.ttf", 11)
inventoryfont = pygame.font.Font("fonts/pixel_font.ttf", 25)
settingsfont = pygame.font.Font("fonts/Minecraft.ttf", 25)

# game over screen
game_over_image = pygame.transform.scale(pygame.image.load("images/screens/game_over.png"), (1280, 720))

# SCREEN RESOLUTION
resolution = (1280, 720)  # height/width

width, height = resolution[0], resolution[1]
fps = 60
# screen = pygame.display.set_mode(resolution)
# some screen images
pause_image = pygame.transform.scale(pygame.image.load("images/others/pause_image2.png"), (1280, 180))
choose_character_image = pygame.transform.scale(pygame.image.load("images/screens/choose_character.png"), resolution)
# menu of the store
menu_store = pygame.transform.scale(pygame.image.load("images/store/menu_store.png"), (750, 600))
entrance_store = pygame.transform.scale(pygame.image.load("images/store/store_front.png"), resolution)

# OLD LADY SPEECHES
# old_lady_1 = pygame.transform.scale(pygame.image.load("images/others/old_lady_speech1.png"), (150, 100))
# old_lady_2 = pygame.transform.scale(pygame.image.load("images/others/old_lady_speech2.png"), (150, 100))
# old_lady_3 = pygame.transform.scale(pygame.image.load("images/others/old_lady_speech3.png"), (150, 100))
old_lady_1 = "Be careful out there!"
old_lady_2 = "Good to see you!"
old_lady_3 = "Looking for something?"
old_lady_4 = "You're not alone, kid."


old_lady_speech = [old_lady_1, old_lady_2, old_lady_3, old_lady_4]

# POWER UP IMAGES
power_up_invincibility = pygame.transform.scale(pygame.image.load("images/others/power_up1.png"), (50, 50))
power_up_speed = pygame.transform.scale(pygame.image.load("images/others/power_up2.png"), (50, 50))
power_up_de_spawner = pygame.transform.scale(pygame.image.load("images/others/power_up3.png"), (50, 50))

# SIZES
player_size = (40, 40)
dog_size = (30, 30)
enemy_size = (80, 80)
bullet_size = 10
tile_size = 16
# using the clock to control the time frame
clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution)
mouse = pygame.mouse.get_pos()
character_choice = "player 1"


# this is to store progress when the game is closed
def progress():
    with open("player_info.txt", "w") as player_file:
        json.dump(info, player_file)


# Function to draw the music bar
def music_bar(screen, bar_x, bar_y, bar_width, bar_height, global_volume):

    # Draw the plus and minus buttons
    minus_button = draw_button(screen, bar_x - 70 - 10, bar_y + (bar_height - 80) // 2, 70, 80, 'MINUS', white, 'images/store/store_button.png', cutefont)
    plus_button = draw_button(screen, bar_x + bar_width + 10, bar_y + (bar_height - 80) // 2, 70, 80, 'PLUS', white, 'images/store/store_button.png', cutefont)

    # Draw the main bar
    pygame.draw.rect(screen, brick_color, (bar_x, bar_y, bar_width, bar_height))

    # Draw the slider
    slider_x = bar_x + (global_volume * bar_width) - (bar_height // 2)
    pygame.draw.rect(screen, white, (slider_x, bar_y - (bar_height // 2), bar_height, bar_height * 2))

    return minus_button, plus_button


