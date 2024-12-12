from config import *
import pygame


# if I am not mistaken it works only between a moving object and a static object
class CollisionObject(pygame.sprite.Sprite):
    def __init__(self, position, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)
