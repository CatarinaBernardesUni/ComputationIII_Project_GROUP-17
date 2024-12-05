from random import random
from config import *
from math import atan2, degrees
import pygame.sprite

# todo: a lot of this definitions are for weapons in the diagonal
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, name, tier, damage, range, attack_speed, durability,
                 crit_chance, crit_multiplier, groups, special_effect=None):
        super().__init__(groups)

        # weapon attributes
        self.name = name
        self.tier = tier
        self.damage = damage
        self.range = range
        self.attack_speed = attack_speed
        self.durability = durability
        self.crit_chance = crit_chance  # probability of dealing extra damage
        self.crit_multiplier = crit_multiplier  # how much extra damage is dealt
        self.special_effect = special_effect  # burn, freeze, maybe more efficient in some players than others
        self.usage_count = 0

        # connection to the player
        self.player = player
        self.distance = 50
        self.player_direction = pygame.Vector2(0, 1)  # weapon at the right (i think) of the player

        self.weapon_surf = pygame.image.load(
            "images/weapons/fire_sword/fire1.png").convert_alpha()
        self.scaled_weapon_surf = pygame.transform.scale(self.weapon_surf, (35, 35))
        self.image = self.scaled_weapon_surf
        self.rect = self.image.get_rect(center=self.player.rect.center + self.player_direction * self.distance)

    def update(self):
        self.get_direction()
        self.rotate_weapon()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

    def rotate_weapon(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        print(angle)
        if -45 <= angle <= 45:
            self.image = pygame.transform.rotate(self.scaled_weapon_surf, angle)
        elif 45 < angle <= 90 or -270 <= angle < -225:
            self.image = pygame.transform.rotate(self.scaled_weapon_surf, angle - 90)
        elif -225 <= angle < -135:
            flipped_image = pygame.transform.flip(self.scaled_weapon_surf, False, True)
            self.image = pygame.transform.rotate(flipped_image, angle)
        elif -135 <= angle < -45:
            # flipped_image = pygame.transform.flip(self.scaled_weapon_surf, True, False)
            self.image = pygame.transform.rotate(self.scaled_weapon_surf, angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_direction(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        player_position = pygame.Vector2(self.player.rect.center)
        self.player_direction = (mouse_position - player_position).normalize()

    def attack(self, target):
        if self.durability <= 0:
            return "This weapon is broken"
            # todo: check if I should use a return or a print here

        damage_dealt = self.damage
        if self.roll_crit():
            damage_dealt *= self.crit_multiplier

        if self.special_effect:
            self.apply_effect(target)

        self.durability -= 1
        self.usage_count += 1
        self.adapt()

        return damage_dealt

    def roll_crit(self):
        return random() <= self.crit_chance

    def apply_effect(self, target):
        if self.special_effect == "burn":
            target.take_damage(5)
        elif self.special_effect == "freeze":
            target.slow(50)
        elif self.special_effect == "stun":
            target.kill()

    def upgrade(self):
        if self.tier < 5:
            self.tier += 1
            self.damage *= 1.2
            self.range += 1
            self.attack_speed *= 1.1
            self.durability += 10
            self.crit_chance += 0.02

    def break_weapon(self):
        self.durability = 0
        # todo: decide what to do when a weapon breaks

    def repair(self):
        self.durability = 100

    def display_stats(self):
        print(f"Name: {self.name}")
        print(f"Tier: {self.tier}")
        print(f"Damage: {self.damage}")
        print(f"Range: {self.range}")
        print(f"Attack Speed: {self.attack_speed}")
        print(f"Durability: {self.durability}")
        print(f"Crit Change: {self.crit_chance*100}%")
        print(f"Crit Multiplier: {self.crit_multiplier}")
        print(f"Special Effect: {self.special_effect}")
        print(f"Usage Count: {self.usage_count}")

    def adapt(self):
        if self.usage_count % 10 == 0:
            self.damage += 1 # increase damage every 10 attacks

#weapons = {Weapon(name="Flaming Sword",tier=1,damage=20,range=5,attack_speed=1.5,durability=50,crit_chance=0.1,crit_multiplier=2.0,special_effect="burn"),
    # Weapon(name="Frost Axe",tier=2,damage=15,range=3,attack_speed=1.2,durability=40,crit_chance=0.15,crit_multiplier=2.0,special_effect="freeze"),
    # Weapon(name="Thunder Hammer",tier=3,damage=25,range=2,attack_speed=0.8,durability=30,crit_chance=0.1,crit_multiplier=1.8,special_effect="stun"),
    # Weapon(name="Iron Sword",tier=1,damage=10,range=3,attack_speed=1.5,durability=50,crit_chance=0.05,crit_multiplier=1.5,special_effect=None)}

