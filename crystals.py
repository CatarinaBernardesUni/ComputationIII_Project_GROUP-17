import pygame
crystals_data = {"red_crystal": "images/crystals/Dark_red_ crystal2.png",
                 "blue_crystal": "images/crystals/Blue_crystal2.png",
                 "gold_crystal": "images/crystals/Yellow_crystal2.png",
                 "purple_crystal": "images/crystals/Violet_crystal2.png",
                 "white_crystal": "images/crystals/White_crystal2.png"}
# crystal is not a sprite class because it doesn't need to be updated
class Crystal:
    def __init__(self, name, crystals_data):
        # stripped_crystals = [item.replace("_crystal", "") for item in crystals_data.keys()]
        self.name = name
        self.image = pygame.image.load(crystals_data[name])

