from config import *
import pygame
from os import walk  # allows us to walk through a folder
from os.path import join


class Dog(pygame.sprite.Sprite):
    """
    This class represents a dog that follows the player around in the main area of the game and in the battlefield.
    The dog is set to False until the player buys it in the store, only then it will execute.

    Attributes
    ----------
    player : Player
        The player sprite that the dog will follow.
    dog_size : tuple
        The dimensions (width, height) of the dog sprite.
    state : str
        The current state of the dog's animation (e.g., "down").
    frame_index : int
        The index of the current animation frame.
    image : pygame.Surface
        The current visual representation of the dog sprite.
    rect : pygame.Rect
        The rectangle defining the position and dimensions of the dog for rendering and collision purposes.
    bought : bool
        Indicates whether the dog has been purchased by the player (True) or not (False).

    Parameters
    ----------
    player: Player
        the player sprite that the dog will follow.

    """
    def __init__(self, player):
        super().__init__()
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
        """
        This function loads the image of the dog for its animation.
        Also, scales the dog size and converts its image for transparency.
        """
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
                        scaled_surf = pygame.transform.scale(surf, dog_size)
                        self.frames[state].append(scaled_surf)

    def animate(self):
        """
        Animates the dog by updating its frame index, so the speed of the movement.
        """
        self.frame_index += 0.08  # increments frame index at a fixed fps (animation speed)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def follow_player(self):
        """
        Allows the dog to follow the player, so each direction the player moves, the dog moves. Also mimics the states of the player.
        Updates the dog's position and state based on the player. Then calls the animate function to animate the dog's movements.

        """
        # Determine the direction to follow the player.
        # mimics the actions fo the player
        self.state = self.player.state

        # FOLLOWS PLAYER
        self.rect.x = self.player.rect.x - 30  # so it is a little behind the player
        self.rect.y = self.player.rect.y

        self.animate()