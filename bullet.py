from config import *
import math
import pygame


# everything that moves has to be a child of sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.direction = direction
        self.radius = 10
        self.color = yellow
        #self.image = pygame.image.load("images/others/trident.png")
        #self.image = pygame.surface.Surface(bullet_size)
        # #self.image = pygame.transform.scale(self.image, bullet_size)

        # updating the x and y positions to fit the circle
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.speed = 7  # todo: change the speed when catching a powerup

    def update(self):
        # updating the bullets position based in the speed and direction
        # (x, y) --> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

    def draw(self, screen):  # I changed the screen to display at home
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
