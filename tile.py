import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, surf, groups, frames_animation=None, animation_duration=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=position)
        self.current_anim_index = 0  # Initialize animation index
        self.animation_frames = frames_animation if frames_animation else []  # Store animation frames
        self.animation_duration = animation_duration if animation_duration else 1
        self.animation_time = 0  # Store time passed for animation

    def update(self, time_frame):
        if self.animation_frames:
            self.animation_time += time_frame
            if self.animation_time >= self.animation_duration:
                self.current_anim_index += 1
                if self.current_anim_index >= len(self.animation_frames):
                    self.current_anim_index = 0
                self.image = self.image = self.animation_frames[self.current_anim_index]
                self.animation_time = 0

