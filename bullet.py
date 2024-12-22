from config import *
import math
import pygame
import os

# everything that moves has to be a child of sprite
class Bullet(pygame.sprite.Sprite):
    """
    A class representing a bullet/arrows in the game, with movement, animation, and killing if it leaves the screen.

    Parameters
    ----------
    x : int
        The initial x-coordinate of the bullet's center.
    y : int
        The initial y-coordinate of the bullet's center.
    direction : float
        The direction of the bullet's movement in radians.

    Attributes
    ----------
    direction : float
        The direction of the bullet's movement in radians.
    animation_path : str
        The file path to the bullet's animation frames.
    animation_speed : float
        The speed of the bullet's animation cycling.
    current_frame_index : int
        The current frame index in the animation sequence.
    speed : int
        The speed of the bullet's movement.
    frames : list of pygame.Surface
        The list of animation frames loaded from the animation path.
    image : pygame.Surface
        The current surface image of the bullet.
    rect : pygame.Rect
        The rectangle of the bullet.
    """
    def __init__(self, x, y, direction):
        """
        Initializes a Bullet object, loads animation frames, and sets the initial position and direction.

        Parameters
        ----------
        x : int
            The x-coordinate of the bullet's center starting position.
        y : int
            The y-coordinate of the bullet's center starting position.
        direction : float
            The angle of movement in radians (calculated using atan2).
        """
        super().__init__()

        self.direction = direction
        self.animation_path = "images/weapons/blue_arrow"
        self.animation_speed = 0.1
        self.current_frame_index = 0
        self.speed = 4
        # Load animation frames
        self.frames = []
        folder_path = os.path.normpath(self.animation_path)
        for file_name in os.listdir(folder_path):
            frame = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            scaled_frame = pygame.transform.scale(frame, (35, 35))
            self.frames.append(scaled_frame)

        self.image = self.frames[self.current_frame_index]
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.direction))  # Rotate the initial frame
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Updates the position, animation, and state of the bullet (being displayed or "killed").

        Moves the bullet in the direction specified by its speed and angle, handles off-screen killing,
        and animates the bullet by cycling through frames.

        Notes
        -----
        - The bullet is removed from the sprite group if it moves off the screen.
        - Animation frames are cycled based on the animation speed.

        """
        # updating the bullets position based in the speed and direction
        # (x, y) --> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

        # Animate the bullet
        self.animation_speed += 0.9
        if self.animation_speed >= 1:
            self.animation_speed = 0  # Reset the timer
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0
            self.image = self.frames[self.current_frame_index]
            self.image = pygame.transform.rotate(self.image, -math.degrees(self.direction))