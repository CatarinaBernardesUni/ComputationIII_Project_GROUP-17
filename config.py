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


# hearts
full_heart = pygame.transform.scale(pygame.image.load("images/others/full_heart.png"), (33, 33))
empty_heart = pygame.transform.scale(pygame.image.load("images/others/empty_heart.png"), (33, 33))


# font for the game
cutefont = pygame.font.Font("fonts/pixel_font.ttf", 11)
inventoryfont = pygame.font.Font("fonts/pixel_font.ttf", 25)

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

#options screen
options_1 = pygame.transform.scale(pygame.image.load("images/screens/options1.png"), resolution)
options_2 = pygame.transform.scale(pygame.image.load("images/screens/options2.png"), resolution)

options_pages = [options_1, options_2]

# menu of the store
menu_store = pygame.transform.scale(pygame.image.load("images/store/menu_store.png"), (750, 600))
entrance_store = pygame.transform.scale(pygame.image.load("images/store/store_front.png"), resolution)

# OLD LADY SPEECHES
old_lady_1 = "Be careful out there!"
old_lady_2 = "Good to see you!"
old_lady_3 = "Looking for something?"
old_lady_4 = "You're not alone, kid."
old_lady_5 = "I'm always here for you."
old_lady_6 = "Are you hungry?"
old_lady_7 = "I'm so proud of you..."

old_lady_speech = [old_lady_1, old_lady_2, old_lady_3, old_lady_4, old_lady_5, old_lady_6, old_lady_7]

# POWER UP IMAGES, these are small because they will appear on top of the player
# the ones that are sized to be on the screen are on the dictionary in power up manager
power_up_invincibility = pygame.transform.scale(pygame.image.load("images/others/power_up1.png"), (25, 25))
power_up_speed = pygame.transform.scale(pygame.image.load("images/others/power_up2.png"), (25, 25))
power_up_de_spawner = pygame.transform.scale(pygame.image.load("images/others/power_up3.png"), (25, 25))
power_up_invisible = pygame.transform.scale(pygame.image.load("images/others/power_up4.png"), (25, 25))

chest_choice = pygame.transform.scale(pygame.image.load("images/chests/chest_choice.png"), (1000, 300))
pick_powerup = pygame.transform.scale(pygame.image.load("images/chests/pick_powerup.png"), (400, 100))

# SIZES
player_size = (40, 40)
dog_size = (30, 30)
enemy_size = (80, 80)
bullet_size = 10
tile_size = 16
# using the clock to control the time frame
clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution)
character_choice = "player 1"
display = pygame.Surface((width // 2, height // 2))


# this is to store progress when the game is closed
def progress():
    with open("player_info.txt", "w") as player_file:
        json.dump(info, player_file)
