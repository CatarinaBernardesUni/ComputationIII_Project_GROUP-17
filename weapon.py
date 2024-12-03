from random import random

import pygame.sprite


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, name, tier, damage, range, attack_speed, durability,
                 crit_chance, crit_multiplier, groups, special_effect=None):
        super.__init__(groups)
        self.image = pygame.image.load() # todo: add an image
        self.rect = self.image.get_rect()

        # weapon atrributes
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
        self.distance = 140
        self.player_direction = pygame.Vector2(1,0)

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

weapons = {Weapon(
    name="Flaming Sword",
    tier=1,
    damage=20,
    range=5,
    attack_speed=1.5,
    durability=50,
    crit_chance=0.1,
    crit_multiplier=2.0,
    special_effect="burn"
), Weapon(
    name="Frost Axe",
    tier=2,
    damage=15,
    range=3,
    attack_speed=1.2,
    durability=40,
    crit_chance=0.15,
    crit_multiplier=2.0,
    special_effect="freeze"
), Weapon(
    name="Thunder Hammer",
    tier=3,
    damage=25,
    range=2,
    attack_speed=0.8,
    durability=30,
    crit_chance=0.1,
    crit_multiplier=1.8,
    special_effect="stun"
), Weapon(
    name="Iron Sword",
    tier=1,
    damage=10,
    range=3,
    attack_speed=1.5,
    durability=50,
    crit_chance=0.05,
    crit_multiplier=1.5,
    special_effect=None
)
}