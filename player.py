from config import *
import pygame
import math
from bullet import Bullet
from os.path import join
from os import walk  # allows us to walk through a folder
import config
from dog import Dog
from weapon import *


# I had to import the module itself here in import config, so we could actually choose a character, I tried for a
# long time and found no other way, I found it was the only way to connect the player to the game without
# importing the game in player because it causes a circular import :')


# making a player a child of the Sprite class

def remove_health(health_being_removed):
    if info['health'] >= 0:
        info['health'] -= health_being_removed


class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame

    def __init__(self):
        # calling the mother classes init aka Sprite
        super().__init__()
        self.font = pygame.font.Font("fonts/pixel_font.ttf", 16)
        self.user = config.character_choice
        self.load_images()  # we need to do this before creating image
        self.state, self.frame_index = "left", 0
        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)  # we use surface to display any image or draw
        # area where the player will be drawn
        self.rect = self.image.get_rect()
        # initial position of the player
        self.rect.center = (1150, 150)
        # making the hitbox smaller than the player image
        self.hitbox_rect = self.rect.inflate(-10, -15)

        # being able to receive a dog:
        self.dog = Dog(self)

        # GAMEPLAY VARIABLES
        self.just_left_cave = False
        self.just_left_old_lady_house = False
        self.just_left_home = False
        self.just_left_store = False
        self.is_fighting = False
        self.is_leaving_battle = False
        self.speed = 1.8
        self.health = info['health']

        self.max_health = 5
        # to be able to pick up hearts in the game
        self.bullet_cooldown = 0
        self.damage_cooldown = 0  # Initial cooldown time
        self.cooldown_duration = 2000  # Cooldown duration in milliseconds

        # INVENTORY AND MONEY (GOLD) START WITH 1200
        self.inventory = {'apple': 0,
                          'mushroom': 0,
                          'speed potion': 0,
                          'dog': 0,
                          'soup': 0,
                          'sword': 0,
                          'bow': 0,
                          'key': 0}
        self.gold = 1200

        # storing the inventory prices
        self.price_items = {'apple': 5,
                            'mushroom': 10,
                            'speed potion': 25,
                            'dog': 50,
                            'soup': 60,
                            'sword': 80,
                            'bow': 100,
                            'key': 300}

        ########### WEAPONS ########################
        self.weapons = {key: None for key in weapons}  # A dictionary to store weapon instances
        self.active_weapon = None  # Currently active weapon
        self.active_weapon_group = pygame.sprite.Group()  # Group to store the active weapon
        ###########################################

    ############################## METHODS TO DEAL WITH WEAPONS ########################################
    def add_weapon(self, weapon_name, weapon_type):
        """Add a weapon instance to the player's inventory."""
        if weapon_type == "Sword":
            weapon_instance = Sword(self, self.active_weapon_group, weapon_name)
        elif weapon_type == "Bow":
            weapon_instance = Bow(self, self.active_weapon_group, weapon_name)
        else:  # a weapon will always be one of these 3 types
            weapon_instance = Axe(self, self.active_weapon_group, weapon_name)

        self.weapons[weapon_name] = weapon_instance

        if not self.active_weapon:  # Auto-select the first weapon if none is active
            self.active_weapon = weapon_instance
            self.active_weapon_group.add(self.active_weapon)

    def switch_weapon(self, weapon_name: str):
        # todo: mouse clicking on the inventory makes them the primary
        """Switch the currently active weapon."""
        if weapon_name in self.weapons.keys():
            self.active_weapon = self.weapons[weapon_name]
            self.active_weapon_group.add(self.active_weapon)
    ####################################################################################################

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

    def draw_hearts(self, display):
        for heart in range(self.max_health):
            if heart < info['health']:
                display.blit(full_heart, (heart * 33, 5))
            else:
                display.blit(empty_heart, (heart * 33, 5))

    def update(self, collision_sprites, display, frame_time, battle_area_rect=None):
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

        self.animate()
        self.draw_hearts(display)
        self.dont_leave_battle(battle_area_rect)

        if self.active_weapon is None and battle_area_rect is not None:
            if battle_area_rect.colliderect(self.rect):
                message_lines = [
                    "You better find a weapon before you start fighting,",
                    "explore a bit more....",
                    "I heard that there is a store somewhere in here..."]

                # Starting position for the text
                start_x = 100
                start_y = 90
                line_spacing = 30  # Spacing between lines
                # Render each line and blit to the screen
                for i, line in enumerate(message_lines):
                    rendered_text = self.font.render(line, True, white)
                    display.blit(rendered_text, (start_x, start_y + i * line_spacing))

                if self.rect.right > battle_area_rect.left:
                    self.rect.right = battle_area_rect.left

    def dont_leave_battle(self, battle_area_rect):
        if self.is_fighting:
            if self.rect.left < battle_area_rect.left:
                self.rect.left = battle_area_rect.left

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

    def buy_item(self, item_name):
        # getting the item price from the price_items dictionary
        price = self.price_items[item_name]

        # checking if the player has enough money to buy the item
        if self.gold >= price:
            self.gold -= price
            self.inventory[item_name] += 1
            print(f"bought {item_name}: amount {self.inventory[item_name]} money: {self.gold}")
            if item_name == 'dog' and self.dog is None:
                self.dog = Dog(self)
                self.dog.bought = True
            elif item_name == 'sword':
                self.add_weapon("dagger", "Sword")
                print(self.weapons)
                print(self.active_weapon)
            elif item_name == 'bow':
                self.add_weapon("ghost_bow", "Bow")
                print(self.weapons)
                print(self.active_weapon)
        else:
            print(f"gold is not enough. gold: {self.gold}")  # todo: add here a screen saying not enough money

    def add_gold(self, amount):
        self.gold += amount
