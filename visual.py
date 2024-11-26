from config import *
import pygame
from utils import *
from mouse_position import *

"""
creating a sprite class for my visuals that will interact when collided with

"""
class Visual(pygame.sprite.Sprite):
    def __init__(self, width, height, visual_path, collision_behaviour):
        super().__init__()

        # setting up the width and height of my visual
        self.width = width
        self.height = height

        # setting up my behaviour for collision
        self.collision_behaviour = collision_behaviour



        ##### CREATING MY VISUAL ######
        # creating my image provided by input
        self.visual_image = pygame.image.load(visual_path)
        # scaling the image accordingly
        self.visual_image = pygame.transform.scale(self.visual_image, (self.width, self.height))

        # creating an area in which when collided against, it will activate
        self.detect_coll = self.visual_image.get_rect()

        # creating a new variable to be able to move the image
        self.visual_pos = self.detect_coll.topleft

    # creating a function to change the visual around
    def set_position(self, x, y):
        self.visual_pos = (x, y)
        self.detect_coll.topleft = (x, y)

    # creating a function to draw the visual on screen
    def draw_visual(self, screen):
        screen.blit(self.visual_image, self.visual_pos)

    def collide_player(self, player):
        if self.detect_coll.colliderect(player.rect):
            self.collision_behaviour(player)

    #def on_collision(self, player):
        #pass

class House(Visual):
    def __init__(self, width, height, visual_path, collision_behaviour):
        super().__init__(width=width, height=height, visual_path=visual_path, collision_behaviour=collision_behaviour)


class Clues(Visual):
    def __init__(self, width, height, visual_path, collision_behaviour):
        super().__init__(width=width, height=height, visual_path=visual_path, collision_behaviour=collision_behaviour)



def get_clue(player):
    background = pygame.image.load("images/GRASS.jpg")
    background = pygame.transform.scale(background, resolution)

    screen = pygame.display.set_mode(resolution)

    # setting up the back button
    back_button = activate_back_button(screen, background, 1050, 620, 140, 60, "back", deep_black, white)

    # trying to make the player move but not working
    # so it doesn't collide with the thing again

    # setting up the background
    screen.blit(background, (0, 0))


def inside_house(player):
    # setting up a background
    background = pygame.image.load("images/inside_house.png")
    background = pygame.transform.scale(background, resolution)
    clue = Clues(100, 100, "images/pregaminho.png", collision_behaviour=get_clue)
    clue.set_position(1000, 200)

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

    # creating special collision area
    special_area = clue.detect_coll

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

        # let the player be able to collide with clue
        # updating player position
        player.update()

        # detect if the user walked in to the special area (which is the house)
        if special_area.colliderect(player.rect):
            clue.collide_player(player)

            # changing the players position to a set one to avoid colliding from the sides.
            # location based on the clue
            player.rect.x = 1050
            player.rect.y = 300

        # displaying the background
        screen.fill(deep_black)
        screen.blit(background, (0, 0))
        back_button_rect = draw_button(screen, 1050, 620, 140, 60, "back", deep_black, white)
        clue.draw_visual(screen)

        # updating player position
        player_group.update()

        # drawing the player
        player_group.draw(screen)

        # updating the display
        pygame.display.update()

