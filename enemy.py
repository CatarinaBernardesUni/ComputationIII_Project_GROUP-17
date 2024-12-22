from player import Player
from config import *
import pygame
import random
import math
import os

enemies_data = {"green_slime": {"tier": 1, "health": 20, "speed": 0.8, "attack": 1,
                                "directory_path": "images/monsters/slime_green", "size": (100, 100),
                                "animation_speed": 0.05, "inflate_parameters": (-50, -50)},

               "normal_fly": {"tier": 1, "health": 15, "speed": 1.2, "attack": 1, "weakness": "fire",
                              "directory_path": "images/monsters/normal_fly", "size": (50, 50),
                              "animation_speed": 0.1, "inflate_parameters": (-10, -15)},

               "fire_fly": {"tier": 2, "health": 40, "speed": 1.5, "attack": 2, "weakness": "ice",
                            "directory_path": "images/monsters/fire_fly", "size": (65, 65),
                            "animation_speed": 0.2, "inflate_parameters": (-10, -15)},

               "horse_ghost": {"tier": 3, "health": 80, "speed": 1.3, "attack": 2.5,
                               "directory_path": "images/monsters/horse_ghost", "size": (70, 70),
                               "animation_speed": 0.3, "inflate_parameters": (-10, -15)},

               "electric_fly": {"tier": 3, "health": 60, "speed": 1.7, "attack": 2,
                                "directory_path": "images/monsters/electric_fly", "size": (100, 100),
                                "animation_speed": 0.0005, "inflate_parameters": (-10, -15)},

               "myst_ghost": {"tier": 4, "health": 120, "speed": 1.5, "attack": 3,
                              "directory_path": "images/monsters/myst_ghost", "size": (60, 90),
                              "animation_speed": 0.05, "inflate_parameters": (-10, -15)},

               "electric_enemy": {"tier": 4, "health": 100, "speed": 1.8, "attack": 3,
                                  "directory_path": "images/monsters/electric_enemy", "size": (100, 100),
                                  "animation_speed": 0.05, "inflate_parameters": (-10, -15)}}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, groups, enemy_name, battle_area_rect):
        super().__init__(groups)

        enemy_data = enemies_data[enemy_name]
        self.name = enemy_name
        self.tier = enemy_data["tier"]
        self.health = enemy_data["health"]
        self.speed = enemy_data["speed"]
        self.attack = enemy_data["attack"]
        self.directory_path = enemy_data["directory_path"]
        self.animation_speed = enemy_data["animation_speed"]
        self.size = enemy_data["size"]
        self.inflate_parameters = enemy_data["inflate_parameters"]
        # Reference to player for targeting
        self.player = player
        self.battle_area_rect = battle_area_rect

        # Load enemy images
        self.frames = []
        folder_path = os.path.normpath(self.directory_path)
        for file_name in os.listdir(folder_path):
            frame = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            self.frames.append(pygame.transform.scale(frame, self.size))

        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]

        # loop to make the enemy not spawn on top of the player
        while True:

            spawn_x = random.randint(
                max(self.battle_area_rect.left, self.player.rect.x - 400),
                min(self.battle_area_rect.right, self.player.rect.x + 400)
            )
            spawn_y = random.randint(
                max(self.battle_area_rect.top, self.player.rect.y - 400),
                min(self.battle_area_rect.bottom, self.player.rect.y + 400)
            )

            # Set the enemy's rectangle
            self.rect = self.image.get_rect(topleft=(spawn_x, spawn_y))

            # Check if the enemy's rect overlaps the player's rect
            if not self.rect.colliderect(self.player.rect):
                break

        self.hitbox_rect = self.rect.inflate(self.inflate_parameters[0], self.inflate_parameters[1])

        # enemies are dying too quickly so the cooldown will make them not loose heath for the whole period of time
        # in which the weapon or arrow are colliding with them
        self.last_hit_time = 0
        self.hit_cooldown = 500

    def update_hitbox(self):
        """Align the hitbox with the rect."""
        self.hitbox_rect.center = self.rect.center

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

        # Update hitbox position
        self.update_hitbox()

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

    def update(self, frame_time):
        if not self.player.invisible:
            self.moves_towards_player()
        self.animate(frame_time)

