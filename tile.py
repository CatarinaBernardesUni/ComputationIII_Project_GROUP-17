import pygame


class Tile(pygame.sprite.Sprite):
    """
    Initialize a Tile sprite.

     Attributes
    ----------
    image : pygame.Surface
        The current visual representation of the tile.
    rect : pygame.Rect
        The rectangle defining the position and dimensions of the tile for rendering and collisions.
    current_anim_index : int
        The index of the current frame in the animation sequence.
    animation_frames : list of pygame.Surface
        A list of surfaces representing the animation frames for the tile. Empty if no animation is provided.
    animation_duration : float
        The duration (in seconds) for each animation frame. Defaults to 1 if not specified.
    animation_time : int
        The elapsed time used to track the animation progress.

    Parameters
    ----------
    position: tuple
        The (x, y) position of the tile.
    surf: pygame.Surface
        The surface representing the tile.
    groups: abstract group of pygame.sprite.Group
        The sprite groups the tile belongs to.
    frames_animation: list, optional
        A list of surfaces for animation frames.
    animation_duration: float, optional
        The duration for each animation frame.

    """

    def __init__(self, position, surf, groups, frames_animation=None, animation_duration=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=position)
        self.current_anim_index = 0  # Initialize animation index
        self.animation_frames = frames_animation if frames_animation else []  # Store animation frames
        self.animation_duration = animation_duration if animation_duration else 1
        self.animation_time = 0  # Store time passed for animation

    def update(self, time_frame, loop=True):
        """
        Update the tile's animation.

        Parameters
        ----------
        time_frame: float
            The time passed since the last update.
        loop: bool, optional
            Whether the animation should loop. Default is True.

        """
        if self.animation_frames:
            self.animation_time += time_frame
            if self.animation_time >= self.animation_duration:
                self.animation_time = 0
                if self.current_anim_index < len(self.animation_frames) - 1:
                    # Move to the next frame if not at the last frame
                    self.current_anim_index += 1
                elif loop:
                    # If we want it to loop, return to the first frame
                    self.current_anim_index = 0
                self.image = self.animation_frames[self.current_anim_index]
