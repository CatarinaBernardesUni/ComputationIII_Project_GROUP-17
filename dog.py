from config import *
import pygame
from os import walk  # allows us to walk through a folder
from os.path import join


class Dog(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()  # just to have a default
        self.load_images()
        # self.load_images()
        self.dog_size = dog_size
        self.state, self.frame_index = "down", 0

        self.image = self.frames[self.state][self.frame_index]  # we use surface to display any image or draw
        # area where the player will be drawn
        self.rect = self.image.get_rect()

        # setting the dog next to the player when it first appears.
        self.rect.x = player.rect.x - 50
        self.rect.y = player.rect.y

        self.player = player
        # making default as False so dog doesn't exist until bought
        self.bought = False
        if info['inventory']['dog'] == 1:
            self.bought = True

    def load_images(self):
        self.frames = {"up": [], "down": [], "left": [], "right": [],
                       "idle_down": [], "idle_up": [], "idle_left": [], "idle_right": []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("images", "dog", state)):
                if file_names:
                    for file_name in file_names:
                        if file_name == ".DS_Store":
                            continue  # Skip .DS_Store files bc its mac for folders creation and creates and error
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert()
                        surf.set_colorkey((0, 0, 0))
                        surf.set_colorkey((255, 255, 255))
                        scaled_surf = pygame.transform.scale(surf, dog_size)
                        self.frames[state].append(scaled_surf)

    def animate(self):
        self.frame_index += 0.08  # increments frame index at a fixed fps (animation speed)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def follow_player(self):
        # Determine the direction to follow the player.
        # mimics the actions fo the player
        self.state = self.player.state

        # FOLLOWS PLAYER
        self.rect.x = self.player.rect.x - 30  # so it is a little behind the player
        self.rect.y = self.player.rect.y

        self.animate()
