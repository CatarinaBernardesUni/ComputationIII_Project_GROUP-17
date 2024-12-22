import math
import os
from random import random
from config import *
from math import atan2, degrees
import pygame.sprite
from abc import ABC, abstractmethod
from bullet import Bullet

weapons = {"dagger": {
    "tier": 1,
    "damage": 18,
    "directory_path": "images/weapons/dagger"},
    "ghost_bow": {
        "tier": 1,
        "damage": 22,
        "directory_path": "images/weapons/ghost_bow"},
    ####################### TIER 2 WEAPONS ########################################
    "winter_sword": {
        "tier": 2,
        "damage": 18,
        "directory_path": "images/weapons/winter_sword"},
    "gold_axe": {
        "tier": 2,
        "damage": 22,
        "directory_path": "images/weapons/gold_axe"},
    ####################### TIER 3 WEAPONS ########################################
    "fire_sword": {
        "tier": 3,
        "damage": 28,
        "directory_path": "images/weapons/fire_sword"},
    "ice_bow": {
        "tier": 3,
        "damage": 24,
        "directory_path": "images/weapons/ice_bow"},
    "light_bow": {
        "tier": 3,
        "damage": 23,
        "directory_path": "images/weapons/light_bow"},
    ####################### TIER 4 WEAPON ########################################
    "ruby_axe": {
        "tier": 4,
        "damage": 15,
        "directory_path": "images/weapons/ruby_axe"}}


class Weapon(pygame.sprite.Sprite, ABC):
    def __init__(self, player, groups, weapon_name):
        super().__init__(groups)

        # weapon attributes
        self.name = weapon_name
        self.tier = weapons[weapon_name]["tier"]
        self.damage = info["weapon_attributes_evolved"][weapon_name]
        self.directory_path = weapons[weapon_name]["directory_path"]

        # connection to the player
        self.player = player
        self.distance = 40
        self.player_direction = pygame.Vector2(0, 1)  # weapon at the right (i think) of the player
        # Matilde said that is left
        # the side of the screen this arrow is pointing to -->

        # Load all weapon frames
        self.frames = []
        folder_path = os.path.normpath(self.directory_path)
        for file_name in os.listdir(folder_path):
            frame = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            scaled_frame = pygame.transform.scale(frame, (35, 35))
            # print(f"Loaded frame: {file_name}")
            self.frames.append(scaled_frame)

        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.current_frame_index]

        self.rect = self.image.get_rect(center=self.player.rect.center + self.player_direction * self.distance)

    #################################### DISPLAY OF WEAPON ###########################################
    @abstractmethod
    def animate(self, frame_time):
        """
        Abstract method to animate the weapon.
        :param frame_time: clock running in the defined fps
        """
        pass

    def update(self, frame_time):
        self.get_direction()
        self.animate(frame_time)
        self.rotate_weapon()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

    @abstractmethod
    def rotate_weapon(self):
        """
        Abstract method to rotate the weapon.
        Implement specific display logic (e.g., rotation, flipping) in child classes.
        """
        pass

    def get_direction(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        player_position = pygame.Vector2(self.player.rect.center)
        self.player_direction = (mouse_position - player_position).normalize()

##################### CHILD CLASSES ############################################
class Sword(Weapon):
    def rotate_weapon(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if -45 <= angle <= 45:
            rotated_frame = pygame.transform.rotate(self.image, angle)
        elif 45 < angle <= 90 or -270 <= angle < -225:
            rotated_frame = pygame.transform.rotate(self.image, angle - 90)
        elif -225 <= angle < -135:
            flipped_image = pygame.transform.flip(self.image, False, True)
            rotated_frame = pygame.transform.rotate(flipped_image, angle)
        else:
            # flipped_image = pygame.transform.flip(self.scaled_weapon_surf, True, False)
            rotated_frame = pygame.transform.rotate(self.image, angle - 90)

        self.image = rotated_frame
        self.rect = self.image.get_rect(center=self.rect.center)

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
        # print(f"Current Frame Index: {self.current_frame_index}")

class Bow(Weapon):
    def __init__(self, player, groups, weapon_name):
        super().__init__(player, groups, weapon_name)
        # self.animation_speed = 0.9
        self.distance = 30
        self.cooldown_time = 1000
        self.last_shot_time = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()

        self.arrow_frames = []
        folder_path = os.path.normpath("images/weapons/blue_arrow")
        for file_name in os.listdir(folder_path):
            frame = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            scaled_frame = pygame.transform.scale(frame, (35, 35))
            # print(f"Loaded frame: {file_name}")
            self.arrow_frames.append(scaled_frame)

    def rotate_weapon(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        flipped_image = pygame.transform.flip(self.image, True, False)
        rotated_frame = pygame.transform.rotate(flipped_image, angle)
        self.image = rotated_frame
        self.rect = self.image.get_rect(center=self.rect.center)

    def animate(self, frame_time):
        self.animation_speed += frame_time
        # Check if it's time to update the animation frame
        if self.animation_speed >= 300:
            self.animation_speed = 0  # Reset the timer
            self.current_frame_index += 1

            # Loop back to the first frame if at the end
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

        self.image = self.frames[self.current_frame_index]
        # print(f"Current Frame Index: {self.current_frame_index}")

    def update(self, frame_time):
        super().update(frame_time)
        self.shoot()
        print(f"Number of bullets: {len(self.bullets)}")
        self.bullets.update()
        for bullet in self.bullets:
            bullet.update()

    def shoot(self):
        print(self.player.rect)
        print(self.rect)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cooldown_time:
            # Calculate bullet direction based on weapon orientation
            angle = atan2(self.player_direction.y, self.player_direction.x)
            # although we are using the direction of the weapon in relation to the player, the arrows were not alining
            # with the animation of the arrow from the bow, so we took out 40 degrees
            angle -= math.radians(40)
            firing_position = self.rect.center
            # Create the bullet
            bullet = Bullet(firing_position[0], firing_position[1], angle)
            # Add the bullet to the group
            self.bullets.add(bullet)
            self.last_shot_time = current_time

class Axe(Weapon):
    def rotate_weapon(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if -90 <= angle <= 90:
            rotated_frame = pygame.transform.rotate(self.image, angle)
        else:
            flipped_image = pygame.transform.flip(self.image, False, True)
            rotated_frame = pygame.transform.rotate(flipped_image, angle)

        self.image = rotated_frame
        self.rect = self.image.get_rect(center=self.rect.center)

    def animate(self, frame_time):
        self.animation_speed += frame_time
        # Check if it's time to update the animation frame
        if self.animation_speed >= 100:
            self.animation_speed = 0  # Reset the timer
            self.current_frame_index += 1

            # Loop back to the first frame if at the end
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

        self.image = self.frames[self.current_frame_index]
