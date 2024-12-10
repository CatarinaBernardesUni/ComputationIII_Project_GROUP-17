from images import dog
from config import *
import pygame
from os import walk  # allows us to walk through a folder
from os.path import join


class Dog(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.load_images()
        self.state, self.frame_index = "down", 0
        self.image = pygame.Surface(dog_size)  # we use surface to display any image or draw
        # area where the player will be drawn
        self.rect = self.image.get_rect()

        # setting the dog next to the player when it first appears.
        self.rect.x = player.rect.x - 50
        self.rect.y = player.rect.y

        self.player = player

        self.bought = False

    def load_images(self):
        self.frames = {"up": [], "down": [], "left": [], "right": [],
                       "idle_down": [], "idle_up": [], "idle_left": [], "idle_right": []}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("images", "dog", state)):
                if file_names:
                    for file_name in file_names:
                        full_path = join(folder_path, file_name)
                        print(f"Attempting to load image: {full_path}")  # Debugging statement
                        if full_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                            try:
                                surf = pygame.image.load(full_path).convert_alpha()
                                scaled_surf = pygame.transform.scale(surf, player_size)
                                self.frames[state].append(scaled_surf)
                                print(f"Successfully loaded image: {full_path}")  # Debugging statement
                            except pygame.error as e:
                                print(f"Unable to load image {full_path}: {e}")
                        else:
                            print(f"Unsupported image format: {full_path}")

    def animate(self):
        self.frame_index += 0.08  # increments frame index at a fixed fps (animation speed)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def follow_player(self):
        self.rect.x = self.player.rect.x - 50
        self.rect.y = self.player.rect.y
