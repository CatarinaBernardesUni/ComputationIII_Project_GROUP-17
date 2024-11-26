from config import *
import pygame

# if I am not mistaken it works only between a moving object and a static object
class CollisionObject(pygame.sprite.Sprite):
    def __init__(self, position, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = position)
