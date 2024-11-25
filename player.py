from config import *
import pygame
import math
from bullet import Bullet
from os.path import join
from os import walk  # allows us to walk through a folder


# making a player a child of the Sprite class
class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    def __init__(self):
        # calling the mother classes init aka Sprite
        super().__init__()
        self.load_images()  # we need to do this before creating image
        self.state, self.frame_index = "left", 0

        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)  # we use surface to display any image or draw
        # area where the player will be drawn
        self.rect = self.image.get_rect()
        # centering the player in its rectangle
        self.rect.center = (width // 2, height // 2)

        # Testing at home: making white become transparent when the player is an image
        # self.image.set_colorkey(white)

        # GAMEPLAY VARIABLES
        self.speed = 3
        self.health = 5
        self.max_health = 5
        # to be able to pick up hearts in the game
        self.bullet_cooldown = 0
        self.damage_cooldown = 0  # Initial cooldown time
        self.cooldown_duration = 2000  # Cooldown duration in milliseconds

    def load_images(self):
        self.frames = {"up": [], "down": [], "left": [], "right": [],
                       "idle_down": [], "idle_up": [], "idle_left": [], "idle_right": []}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("images", "player", "player 3", state)):
                if file_names:
                    for file_name in file_names:
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        scaled_surf = pygame.transform.scale(surf, player_size)
                        self.frames[state].append(scaled_surf)
                        # self.frames[state].append(surf)

    def animate(self):
        self.frame_index += 0.07  # increments frame index at a fixed fps (animation speed)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(full_heart, (heart * 50, 10))
            else:
                screen.blit(empty_heart, (heart * 50, 10))

    def update(self):
        # getting the keys input

        keys = pygame.key.get_pressed()
        movement = False
        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.state = "up"
            movement = True
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
            self.state = "down"
            movement = True
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.state = "left"
            movement = True
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed
            self.state = "right"
            movement = True

        if not movement:
            if self.state == "down":
                self.state = "idle_down"
            elif self.state == "up":
                self.state = "idle_up"
            elif self.state == "left":
                self.state = "idle_left"
            elif self.state == "right":
                self.state = "idle_right"

        if keys[pygame.K_SPACE]:
            pass
        self.animate()
        self.empty_hearts()

    def shoot(self, bullets):
        """
        bullets --> pygame group where I will add bullets
        """
        # todo: different weapons have different cooldowns
        # cooldown ==> how many frames I need to wait until I can shoot again
        if self.bullet_cooldown <= 0:
            # defining the directions in which the bullets will fly
            # these 4 directions, are in order, right, left, up and down
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                # Creating a bullet for each angle
                # I will use self.rect.centerx to make the x position of the bullet the same as the
                # x position of the player, thus making the bullet come out of them
                # finally, the direction of the bullet is the angle
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = fps

        self.bullet_cooldown -= 1
