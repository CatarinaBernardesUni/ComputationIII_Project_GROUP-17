from config import *
import pygame
import math

# needs to follow my plauer
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super().__init__()

        self.direction = direction
        self.radius = bullet_size
        self.color = deep_black

        # updating the x and y positions to fit the circle
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.speed = 7    # it could be affected by other factors like powerups

    def update(self):

        # updating the bullet's position based on the speed and the direction
        # (x, y) ---> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

    def draw(self, screen):
        # drawing the bullet on the screen
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
