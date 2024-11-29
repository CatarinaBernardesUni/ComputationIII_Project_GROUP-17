from config import *
import pygame
import math
from bullet import Bullet
from os.path import join
from os import walk  # allows us to walk through a folder
import config
# I had to import the module itself here in import config, so we could actually choose a character, I tried for a
# long time and found no other way


# making a player a child of the Sprite class

def remove_health():
    if info['health'] > 0:
        info['health'] -= 1


class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    def __init__(self):
        # calling the mother classes init aka Sprite
        super().__init__()
        self.user = config.character_choice
        self.load_images()  # we need to do this before creating image
        self.state, self.frame_index = "left", 0
        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)  # we use surface to display any image or draw
        # area where the player will be drawn
        self.rect = self.image.get_rect()
        # centering the player in its rectangle
        self.rect.center = (1150, 150)
        self.hitbox_rect = self.rect.inflate(-10, -15)  # making the hitbox smaller than the player image
        # todo: change this according to the player image

        # GAMEPLAY VARIABLES
        self.speed = 1.8
        self.health = info['health']

        self.max_health = 5
        # to be able to pick up hearts in the game
        self.bullet_cooldown = 0
        self.damage_cooldown = 0  # Initial cooldown time
        self.cooldown_duration = 2000  # Cooldown duration in milliseconds

        # INVENTORY AND MONEY (GOLD) START WITH 200
        self.inventory = {'apple': 0,
                          'mushroom': 0,
                          'speed potion': 0,
                          'dog': 0}
        self.gold = 200

    def load_images(self):
        self.frames = {"up": [], "down": [], "left": [], "right": [],
                       "idle_down": [], "idle_up": [], "idle_left": [], "idle_right": []}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("images", "player", self.user, state)):
                if file_names:
                    for file_name in file_names:
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        scaled_surf = pygame.transform.scale(surf, player_size)
                        self.frames[state].append(scaled_surf)
                        # self.frames[state].append(surf)

    def animate(self):
        self.frame_index += 0.08  # increments frame index at a fixed fps (animation speed)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def empty_hearts(self):
        for heart in range(self.max_health):
            if heart < info['health']:
                screen.blit(full_heart, (heart * 50, 10))
            else:
                screen.blit(empty_heart, (heart * 50, 10))

    def update(self, collision_sprites):
        # getting the keys input

        keys = pygame.key.get_pressed()
        movement = False
        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.rect.y -= self.speed
            self.state = "up"
            movement = True
            self.hitbox_rect.centery = self.rect.centery
            self.collision('vertical', collision_sprites)
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            self.rect.y += self.speed
            self.state = "down"
            movement = True
            self.hitbox_rect.centery = self.rect.centery
            self.collision('vertical', collision_sprites)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.x -= self.speed
            self.state = "left"
            movement = True
            self.hitbox_rect.centerx = self.rect.centerx
            self.collision('horizontal', collision_sprites)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < width:
            self.rect.x += self.speed
            self.state = "right"
            movement = True
            self.hitbox_rect.centerx = self.rect.centerx
            self.collision('horizontal', collision_sprites)

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

    def collision(self, direction, collision_sprites):
        for sprite in collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    # Resolve horizontal collision
                    if self.rect.centerx < sprite.rect.centerx:  # Moving right
                        overlap = self.hitbox_rect.right - sprite.rect.left
                        self.rect.x -= overlap
                    elif self.rect.centerx > sprite.rect.centerx:  # Moving left
                        overlap = sprite.rect.right - self.hitbox_rect.left
                        self.rect.x += overlap
                elif direction == 'vertical':
                    # Resolve vertical collision
                    if self.rect.centery < sprite.rect.centery:  # Moving down
                        overlap = self.hitbox_rect.bottom - sprite.rect.top
                        self.rect.y -= overlap
                    elif self.rect.centery > sprite.rect.centery:  # Moving up
                        overlap = sprite.rect.bottom - self.hitbox_rect.top
                        self.rect.y += overlap

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

    def get_health(self):  # we should use this if the player picks up hearts or something
        if info['health'] < self.max_health:
            info['health'] += 1
