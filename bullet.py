from config import *
import math
import pygame
import os

from utils import calculate_camera_offset


# everything that moves has to be a child of sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.direction = direction
        self.radius = 10
        self.color = yellow
        self.animation_path = "images/weapons/blue_arrow"
        self.animation_speed = 0.1
        self.current_frame_index = 0
        self.speed = 7
        # Load animation frames
        self.frames = []
        folder_path = os.path.normpath(self.animation_path)
        for file_name in os.listdir(folder_path):
            frame = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            scaled_frame = pygame.transform.scale(frame, (35, 35))
            self.frames.append(scaled_frame)

        self.image = self.frames[self.current_frame_index]
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.direction))  # Rotate the initial frame
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # updating the bullets position based in the speed and direction
        # (x, y) --> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off-screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

        # Animate the bullet
        self.animation_speed += 0.9
        if self.animation_speed >= 1:
            self.animation_speed = 0  # Reset the timer
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0
            self.image = self.frames[self.current_frame_index]
            self.image = pygame.transform.rotate(self.image, -math.degrees(self.direction))

