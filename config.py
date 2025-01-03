import json
import pygame


pygame.init()
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
yellow_torrado = (240, 200, 60)

brick_color_transparent = (117, 49, 40, 225)
brick_color = (117, 49, 40)

# global volume for all music
global_volume = 0.5
menu_music = pygame.mixer.Sound("music/main_menu.mp3")
menu_music.set_volume(global_volume)
battle_music = pygame.mixer.Sound("music/TheGreatBattle.mp3")
battle_music.set_volume(global_volume)
main_music = pygame.mixer.Sound("music/Adventure.mp3")
main_music.set_volume(global_volume)
coin_music = pygame.mixer.Sound("music/coin.wav")
coin_music.set_volume(global_volume)
sparkly_music = pygame.mixer.Sound("music/sparkly.wav")
sparkly_music.set_volume(global_volume)
dog_bark = pygame.mixer.Sound("music/dog_bark.mp3")
dog_bark.set_volume(global_volume)
game_over_sound = pygame.mixer.Sound("music/game_over_sound.wav")
game_over_sound.set_volume(global_volume)

# creating a list of all sounds
all_sounds = [menu_music, battle_music, main_music, coin_music, sparkly_music, dog_bark, game_over_sound]

# font for the game
cutefont = pygame.font.Font("fonts/pixel_font.ttf", 11)
inventoryfont = pygame.font.Font("fonts/pixel_font.ttf", 25)
settingsfont = pygame.font.Font("fonts/Minecraft.ttf", 25)
font_for_message = pygame.font.Font("fonts/pixel_font.ttf", 16)
pixel = pygame.font.SysFont("Pixel", 35)

# game over screen
game_over_image = pygame.transform.scale(pygame.image.load("images/screens/game_over.png"), (1280, 720))

# SCREEN RESOLUTION
resolution = (1280, 720)  # height/width

width, height = resolution[0], resolution[1]
fps = 60

# using the clock to control the time frame
clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution, pygame.SRCALPHA)
character_choice = "player 1"
display = pygame.Surface((width // 2, height // 2))

# some screen images
pause_image = pygame.transform.scale(pygame.image.load("images/screens/pause_image.png"), (1280, 180)).convert_alpha()
pause_image.set_colorkey((0, 0, 0))

choose_character_image = pygame.transform.scale(pygame.image.load("images/screens/choose_character.png"), resolution)

# options screen
rules_1 = pygame.transform.scale(pygame.image.load("images/rules/rules1.png"), resolution)
rules_2 = pygame.transform.scale(pygame.image.load("images/rules/rules2.png"), resolution)
rules_3 = pygame.transform.scale(pygame.image.load("images/rules/rules3.png"), resolution)
rules_4 = pygame.transform.scale(pygame.image.load("images/rules/rules4.png"), resolution)
rules_5 = pygame.transform.scale(pygame.image.load("images/rules/rules5.png"), resolution)
rules_6 = pygame.transform.scale(pygame.image.load("images/rules/rules6.png"), resolution)
rules_7 = pygame.transform.scale(pygame.image.load("images/rules/rules7.png"), resolution)
rules_8 = pygame.transform.scale(pygame.image.load("images/rules/rules8.png"), resolution)
rules_9 = pygame.transform.scale(pygame.image.load("images/rules/rules9.png"), resolution)
rules_pages = [rules_1, rules_2, rules_3, rules_4, rules_5, rules_6, rules_7, rules_8, rules_9]

# menu of the store
menu_store = pygame.transform.scale(pygame.image.load("images/store/menu_store.png"), (750, 600))

# OLD LADY SPEECHES
old_lady_1 = "Be careful out there!"
old_lady_2 = "Good to see you!"
old_lady_3 = "Looking for something?"
old_lady_4 = "You're not alone, kid."
old_lady_5 = "I'm always here for you."
old_lady_6 = "Are you hungry?"
old_lady_7 = "I'm so proud of you..."

old_lady_speech = [old_lady_1, old_lady_2, old_lady_3, old_lady_4, old_lady_5, old_lady_6, old_lady_7]

# hearts
full_heart = pygame.transform.scale(pygame.image.load("images/others/full_heart.png").convert_alpha(), (33, 33))
empty_heart = pygame.transform.scale(pygame.image.load("images/others/empty_heart.png").convert_alpha(), (33, 33))

# POWER UP IMAGES, these are small because they will appear on top of the player
# the ones that are sized to be on the screen are on the dictionary in power up manager
power_up_invincibility = pygame.transform.scale(pygame.image.load("images/others/power_up1.png").convert_alpha(),
                                                (25, 25))
power_up_speed = pygame.transform.scale(pygame.image.load("images/others/power_up2.png").convert_alpha(), (25, 25))
power_up_de_spawner = pygame.transform.scale(pygame.image.load("images/others/power_up3.png").convert_alpha(), (25, 25))
power_up_invisible = pygame.transform.scale(pygame.image.load("images/others/power_up4.png").convert_alpha(), (25, 25))

chest_choice = pygame.transform.scale(pygame.image.load("images/chests/chest_choice.png").convert_alpha(), (1000, 300))
pick_powerup = pygame.transform.scale(pygame.image.load("images/chests/pick_powerup.png").convert_alpha(), (400, 100))
gold_chest = pygame.transform.scale(pygame.image.load("images/chests/chest_with_gold.png").convert_alpha(), (40, 40))

# SIZES
player_size = (40, 40)
dog_size = (30, 30)
enemy_size = (80, 80)
bullet_size = 10
tile_size = 16

try:
    with open("player_info.txt") as player_file:
        info = json.load(player_file)
except (FileNotFoundError, json.JSONDecodeError):
    print('no file created yet.')
    info = info.copy()


def progress():
    """
    Saves the player's progress in a file.

    This function writes the player's information to a file named 'player_info.txt'

    """
    with open("player_info.txt", "w") as player_file:
        json.dump(info, player_file)
