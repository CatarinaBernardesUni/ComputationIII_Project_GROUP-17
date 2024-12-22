from config import *
import pygame


class CollisionObject(pygame.sprite.Sprite):
    """
    Class that represents a static collision object in the game.

    Parameters
     ----------
    position: tuple
        the (x, y) position of the collision object.
    size: tuple
        the (width, height) size of the collision object.
    groups: tuple of pygame.sprite.Group
        the sprite groups that the collision object belongs to.

    """
    def __init__(self, position, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)
