from config import *
import pygame
from utils import *

"""
creating a sprite class for my visuals that will interact when collided with

"""
class Visual(pygame.sprite.Sprite):
    def __init__(self, width, height, visual_path):
        super().__init__()

        # setting up the width and height of my visual
        self.width = width
        self.height = height

        ##### CREATING MY VISUAL ######
        # creating my image provided by input
        self.visual_image = pygame.image.load(visual_path)
        # scaling the image accordingly
        self.visual_image = pygame.transform.scale(self.visual_image, (self.width, self.height))

        # creating an area in which when collided against, it will activate
        self.detect_coll = self.visual_image.get_rect()

    def collide_player(self, player):
        if self.detect_coll.colliderect(player.rect):
            self.on_collision()

    def on_collision(self):
        pass

class House(Visual):
    def __init__(self, width, height, visual_path):
        super().__init__(width=width, height=height, visual_path=visual_path)

    def on_collision(self):
        under_construction()
