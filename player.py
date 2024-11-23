from utils import *
from config import *
import pygame
import math
from bullet import Bullet

# making player a child of the Sprite class:
class Player(pygame.sprite.Sprite):

    def __init__(self):
        # calling the mother class' init
        super().__init__()

        # VISUAL VARIABLES
        # we call surface to represent the player image
        self.image = pygame.Surface(player_size, pygame.SRCALPHA)   # lets support transparent backgrounds
        # drawing the image of the player
        player_image = pygame.image.load("images/character.png")
        player_image = pygame.transform.scale(player_image, player_size)

        # Blit the player image onto the surface
        self.image.blit(player_image, (0, 0))

        # getting player rect
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0

    def update(self):

        # getting the keys input
        keys = pygame.key.get_pressed()

        # checking which keys were pressed and moving the player accordingly
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self, bullets):
        """

        bullets --> pygame group where I will add bullets
        """

        # hint: certain weapons should have different cooldown
        # cooldown ===> how many frames I need to wait until I can shoot again
        if self.bullet_cooldown <= 0:
            # === defining the direction in each the bullets will fly ===
            # these 4 directions are, in order, right, left, up, down
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:

                # ==== CREATING A BULLET FOR EACH ANGLE ======

                # creating a bullet for each angle
                # I will use self.rect.centerx to make the x position of the bullet the same as the
                # x position of the player, thus making the bullet come out of them.
                # finally, the direction of the bullet is the angle
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                # adding the bullet to the bullets pygame group.
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = fps

        self.bullet_cooldown -= 1
