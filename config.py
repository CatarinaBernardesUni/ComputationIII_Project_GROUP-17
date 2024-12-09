# Config file used to set global variables and other settings
# COLORS AND PICTURES HERE FOR NOW

from progress import *

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


full_heart = pygame.transform.scale(pygame.image.load("images/others/full_heart.png"), (33, 33))
empty_heart = pygame.transform.scale(pygame.image.load("images/others/empty_heart.png"), (33, 33))

game_over_image = pygame.transform.scale(pygame.image.load("images/screens/game_over.png"), (1280, 720))

# SCREEN RESOLUTION
resolution = (1280, 720)  # height/width
# todo: make resolution options in the interface
width, height = resolution[0], resolution[1]
fps = 60
# screen = pygame.display.set_mode(resolution)
pause_image = pygame.transform.scale(pygame.image.load("images/others/pause_image2.png"), (1280, 180))
choose_character_image = pygame.transform.scale(pygame.image.load("images/screens/choose_character.png"), resolution)
# menu of the store
menu_store = pygame.transform.scale(pygame.image.load("images/store/menu_store.png"), (750, 600))
entrance_store = pygame.transform.scale(pygame.image.load("images/store/store_front.png"), resolution)


# SIZES
player_size = (40, 40)
enemy_size = (80, 80)
bullet_size = 10
tile_size = 16
# using the clock to control the time frame
clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution)
mouse = pygame.mouse.get_pos()
character_choice = "player 1"


def progress():
    with open("player_info.txt", "w") as player_file:
        json.dump(info, player_file)
