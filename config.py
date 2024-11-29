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
full_heart = pygame.transform.scale(pygame.image.load("images/others/full_heart.png"), (50, 50))
empty_heart = pygame.transform.scale(pygame.image.load("images/others/empty_heart.png"), (50, 50))
game_over_image = pygame.image.load("images/screens/gameover.png")

#mouse_image = pygame.transform.scale(pygame.image.load("images/others/mouse_image.png"), (50, 50))
# SCREEN RESOLUTION
resolution = (1280, 720)  # height/width
# todo: make resolution options in the interface
width, height = resolution[0], resolution[1]
fps = 60
# screen = pygame.display.set_mode(resolution)
pause_image = pygame.transform.scale(pygame.image.load("images/others/pause_image2.png"), (1280, 180))
# pause_image.get_rect(center=(720 // 2, 100))
choose_character_image = pygame.transform.scale(pygame.image.load("images/screens/choose_character.png"), resolution)

# SIZES
player_size = (40, 40)
enemy_size = (80, 80)
bullet_size = 10
tile_size = 16
# using the clock to control the time frame
clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution)
# pygame.cursors.load_xbm()
mouse = pygame.mouse.get_pos()
character_choice = "player 1"

def progress():
    with open("player_info.txt", "w") as player_file:
        json.dump(info, player_file)

