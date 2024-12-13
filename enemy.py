from config import *
import pygame
import random
import math
import os

enemies = {"green_slime": {"tier": 1, "element": None, "health": 20, "speed": 0.8, "attack": 1, "weakness": "fire",
                           "special_effect": None, "directory_path": "images/monsters/slime_green"},
           "normal_fly": {"tier": 1, "element": None, "health": 15, "speed": 1.2, "attack": 1, "weakness": "fire",
                          "special_effect": None, "directory_path": "images/monsters/normal_fly"},
           "fire_fly": {"tier": 2, "element": "fire", "health": 40, "speed": 1.5, "attack": 2, "weakness": "ice",
                        "special_effect": None, "directory_path": "images/monsters/fire_fly"},
           "horse_ghost": {"tier": 3, "element": "darkness", "health": 80, "speed": 1.3, "attack": 2.5,
                           "weakness": "light", "special_effect": "fear",
                           "directory_path": "images/monsters/horse_ghost"},  # fear makes the player slower
           "electric_fly": {"tier": 3, "element": "electricity", "health": 60, "speed": 1.7, "attack": 2,
                            "weakness": "ice", "special_effect": "shock",
                            "directory_path": "images/monsters/electric_fly"},  # shock makes the player paralysed
           "myst_ghost": {"tier": 4, "element": "darkness", "health": 120, "speed": 1.5, "attack": 3,
                          "weakness": "light", "special_effect": "shoot",
                          "directory_path": "images/monsters/myst_ghost"},
           "electric_enemy": {"tier": 4, "element": "electricity", "health": 100, "speed": 1.8, "attack": 3,
                              "weakness": "ice", "special_effect": "explosion",
                              "directory_path": "images/monsters/electric_enemy"}}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, groups, enemy_name, battle_area_rect):
        super().__init__(groups)

        enemy_data = enemies[enemy_name]
        self.name = enemy_name
        self.tier = enemy_data["tier"]
        self.element = enemy_data["element"]
        self.health = enemy_data["health"]
        self.speed = enemy_data["speed"]
        self.attack = enemy_data["attack"]
        self.weakness = enemy_data["weakness"]
        self.special_effect = enemy_data["special_effect"]
        self.directory_path = enemy_data["directory_path"]

        # Reference to player for targeting
        self.player = player

        # Load enemy images
        self.frames = []
        folder_path = os.path.normpath(self.directory_path)
        for file_name in os.listdir(folder_path):
            frame = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            self.frames.append(pygame.transform.scale(frame, (50, 50)))

        self.animation_speed = 0.1
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect()

        # starting the enemy at random valid location on the screen
        # todo: verify that this is ensuring that the enemies only spawn in the rectangle IT IS NOT
        # self.rect.x = random.randint(0, battle_area_rect.x - enemy_size[0])
        # self.rect.y = random.randint(0, battle_area_rect.y - enemy_size[-1])

    def moves_towards_player(self):
        # determining the direction of the movement based on the player location
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y

        # getting the direction in radius
        direction = math.atan2(dy, dx)

        # moving the enemy towards the player --> like bullet
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

    def animate(self, frame_time):
        self.animation_speed += frame_time
        # Check if it's time to update the animation frame
        if self.animation_speed >= 75:
            self.animation_speed = 0  # Reset the timer
            self.current_frame_index += 1

            # Loop back to the first frame if at the end
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

        self.image = self.frames[self.current_frame_index]

    def apply_special_effect(self):
        # Apply special effects based on enemy type
        # todo: should I add this to the update
        if self.special_effect == "fear":
            self.player.speed *= 0.5
        elif self.special_effect == "shock":  # took out the enemy that had this
            self.player.stunned = True
        elif self.special_effect == "shoot":
            self.shoot()
        elif self.special_effect == "explosion":
            self.explode()

    def shoot(self):
        pass

    def explode(self):
        pass

    def update(self, frame_time):
        self.moves_towards_player()
        self.animate(frame_time)
