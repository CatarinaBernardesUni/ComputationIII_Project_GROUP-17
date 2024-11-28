from utils import *
from config import *
import pygame
import math
from bullet import Bullet

# making a player a child of the Sprite class
class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    def __init__(self):
        # calling the mother classes init aka Sprite
        super().__init__()
        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)  # we use surface to display any image or draw
        # drawing the image of the player
        self.image.fill(cute_purple)
        # area where the player will be drawn
        self.rect = self.image.get_rect()
        # centering the player in its rectangle
        # self.rect.center = (width // 2, height // 2)
        self.rect.center = (1150, 150)
        self.hitbox_rect = self.rect.inflate(0, 0) # making the hitbox smaller than the player image
                                                    # todo: change this according to the player image

        # GAMEPLAY VARIABLES
        self.speed = 3
        self.health = 100
        self.bullet_cooldown = 0

    def update(self, collision_sprites):
        # getting the keys input
        keys = pygame.key.get_pressed()

        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs
        if keys[pygame.K_w] or keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.hitbox_rect.centery = self.rect.centery
            self.collision('vertical', collision_sprites)
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.y += self.speed
            self.hitbox_rect.centery = self.rect.centery
            self.collision('vertical', collision_sprites)
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.hitbox_rect.centerx = self.rect.centerx
            self.collision('horizontal', collision_sprites)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
            self.hitbox_rect.centerx = self.rect.centerx
            self.collision('horizontal', collision_sprites)

    def collision(self, direction, collision_sprites):
        for sprite in collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    # Resolve horizontal collision
                    if self.rect.centerx < sprite.rect.centerx:  # Moving right
                        self.rect.right = sprite.rect.left
                    elif self.rect.centerx > sprite.rect.centerx:  # Moving left
                        self.rect.left = sprite.rect.right
                elif direction == 'vertical':
                    # Resolve vertical collision
                    if self.rect.centery < sprite.rect.centery:  # Moving down
                        self.rect.bottom = sprite.rect.top
                    elif self.rect.centery > sprite.rect.centery:  # Moving up
                        self.rect.top = sprite.rect.bottom

                # Sync the hitbox with the rect after collision
                self.hitbox_rect.center = self.rect.center
    
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