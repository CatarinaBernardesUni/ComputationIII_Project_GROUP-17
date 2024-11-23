from config import *
import pygame
from utils import *
from mouse_position import get_mouse_position

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
            self.on_collision(player)

    def on_collision(self, player):
        pass

class House(Visual):
    def __init__(self, width, height, visual_path):
        super().__init__(width=width, height=height, visual_path=visual_path)

    def on_collision(self, player):
        house_collision()



def house_collision():
    # setting up a background
    background = pygame.image.load("images/inside_house.png")
    background = pygame.transform.scale(background, resolution)

    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    # displaying my background
    screen.blit(background, (0, 0))

    # setting up font and text for going back
    corbelfont = pygame.font.SysFont("Corbel", 50)
    back_text = corbelfont.render("back", True, deep_black)

    while True:
        # getting the mouse position
        mouse = get_mouse_position()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 1050 <= mouse[0] <= 1190 and 600 <= mouse[1] <= 660:
                    return   # return from where it was before


        # drawing the back button
        pygame.draw.rect(screen, white, [1050, 600, 140, 60])
        back_rect = back_text.get_rect(center=(1050 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # Updating our screen
        pygame.display.update()
