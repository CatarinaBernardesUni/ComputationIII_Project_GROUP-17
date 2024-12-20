import json
import pygame

pygame.init()

pixel = pygame.font.SysFont("Pixel", 35)
info = {"health": 4,
        "gold": 200,
        "inventory": {"dog": 0,
                      "apple": 0,
                      "mushroom": 0,
                      "speed potion": 0,
                      "dagger": 0,
                      "soup": 0,
                      "ghost_bow": 0,
                      "key": 0,
                      "winter_sword": 0,
                      "gold_axe": 0,
                      "fire_sword": 0,
                      "ice_bow": 0,
                      "light_bow": 0,
                      "ruby_axe": 0,
                      "red_crystal": 0,
                      "blue_crystal": 0,
                      "gold_crystal": 0,
                      "purple_crystal": 0,
                      "white_crystal": 0},
        "claimed_chest_home": 0,
        "stolen_grandma": 0,
        "current_wave": 1}

try:
    with open("player_info.txt") as player_file:
        info = json.load(player_file)
except (FileNotFoundError, json.JSONDecodeError):
    print('no file created yet.')
    info = info.copy()