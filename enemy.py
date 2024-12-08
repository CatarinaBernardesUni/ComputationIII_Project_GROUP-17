from config import *
import pygame
import random
import math

enemies = {"green_slime": {"tier": 1, "element": None, "health": 20, "speed": 0.8, "attack": 1, "weakness": "fire", "special_effect": None},
           "normal_fly": {"tier": 1, "element": None, "health": 15, "speed": 1.2, "attack": 1, "weakness": "fire", "special_effect": None},
           "fire_fly": {"tier": 2, "element": "fire", "health": 40, "speed": 1.5, "attack": 2, "weakness": "ice", "special_effect": None},
           "horse_ghost": {"tier": 3, "element": "darkness", "health": 80, "speed": 1.3, "attack": 2.5, "weakness": "light", "special_effect": "fear"}, # fear makes the player slower
           "electric_fly": {"tier": 3, "element": "electricity", "health": 60, "speed": 1.7, "attack": 2, "weakness": "ice", "special_effect": "shock"}, # shock makes the player paralysed
           "myst_ghost": {"tier": 4, "element": "darkness", "health": 120, "speed": 1.5, "attack": 3, "weakness": "light", "special_effect": "shoot"},
           "electric_enemy": {"tier": 4, "element": "electricity", "health": 100, "speed": 1.8, "attack": 3, "weakness": "ice", "special_effect": "explosion"}}
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # creating a surface for the enemy
        # self.image = pygame.Surface(enemy_size)
        # filling the surface with chosen enemy colour
        enemy_img1 = pygame.image.load("images/monsters/monster 3/enemy.png")
        self.image = pygame.transform.scale(enemy_img1, enemy_size)

        # self.image.fill(greenish)

        # getting rectangle for positioning
        self.rect = self.image.get_rect()

        # starting the enemy at random valid location on the screen
        self.rect.x = random.randint(0, width - enemy_size[0])
        self.rect.y = random.randint(0, height - enemy_size[-1])

        # todo: different enemies have different speeds

        # setting a random initial speed for the enemy
        self.speed = random.randint(1, 2)

        # setting the health bar
        self.health = 10

    def update(self, player):
        # determining the direction of the movement based on the player location
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        # getting the direction in radius
        direction = math.atan2(dy, dx)

        # moving the enemy towards the player --> like bullet
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)

