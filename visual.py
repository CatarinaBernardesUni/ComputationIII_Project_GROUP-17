from config import *
import pygame
from utils import *
from mouse_position import *

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
        house_collision(player)



def house_collision(player):
    # setting up a background
    background = pygame.image.load("images/inside_house.png")
    background = pygame.transform.scale(background, resolution)

    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    # displaying my background
    screen.blit(background, (0, 0))

    ### SETTING UP SO MY PLAYER APPEARS ON SCREEN ####

    # setting up a clock for fps
    clock = pygame.time.Clock()

    # i want my player to start on the bottom, slightly to the right
    player.rect.x = 270
    player.rect.y = resolution[1] - player.rect.height

    # creating the player group
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # initializing back button to avoid errors
    back_button_rect = None

    ### LOOP SO PLAYER CAN MOVE INSIDE HOUSE ####
    running = True
    while running:
        clock.tick(fps)

        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # can't use button loop as it interferes with main loop :(
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse):
                    return

        # displaying the background
        screen.fill(deep_black)
        screen.blit(background, (0, 0))
        back_button_rect = draw_button(screen, 1050, 620, 140, 60, "back", deep_black, white)

        # updating player position
        player_group.update()

        # drawing the player
        player_group.draw(screen)

        # updating the display
        pygame.display.update()


