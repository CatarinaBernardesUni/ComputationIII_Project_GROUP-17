import pygame
import sys
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, animation_frames=None, animation_duration=None):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.current_anim_index = 0  # Initialize animation index
        self.animation_frames = animation_frames if animation_frames else []  # Store animation frames
        self.animation_duration = animation_duration if animation_duration else 1  # Store the duration for animation frames
        self.animation_time = 0  # Store time passed for animation

    def update(self, frame_time):
        if self.animation_frames:
            self.animation_time += frame_time
            if self.animation_time >= self.animation_duration:
                self.current_anim_index += 1
                if self.current_anim_index >= len(self.animation_frames):
                    self.current_anim_index = 0
                self.image = self.image = self.animation_frames[self.current_anim_index]
                self.animation_time = 0


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

tmx_data = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")

sprite_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
animated_tiles_group = pygame.sprite.Group()

# static tiles
for layer in tmx_data.layers:
    if hasattr(layer, "data"):
        for x, y, surface in layer.tiles():
            pos = (x * 16, y * 16)
            Tile(pos=pos, surface=surface, groups=(sprite_group, tiles_group))

    # animated tiles
for layer in tmx_data.layers:  # Loop through layers again for animated tiles
    if hasattr(layer, "data"):
        for x, y, surface in layer.tiles():
            gid = layer.data[y][x]  # Get the gid for the current tile
            if gid in tmx_data.tile_properties:
                props = tmx_data.tile_properties[gid]
                animation_frames = []
                total_duration = 0

                for animation_frame in props.get("frames", []):
                    image = tmx_data.get_tile_image_by_gid(animation_frame.gid)
                    duration = animation_frame.duration
                    animation_frames.append(image)
                    total_duration += duration

                if animation_frames:
                    pos = (x * 16, y * 16)  # Calculate position based on tile coordinates
                    Tile(pos=pos, surface=animation_frames[0], groups=(sprite_group, animated_tiles_group),
                         animation_frames=animation_frames, animation_duration=total_duration)


for obj in tmx_data.objects:
    if obj.image:
        scaled_image = pygame.transform.scale(obj.image, (obj.width, obj.height))
        pos = (obj.x, obj.y)
        Tile(pos=pos, surface=scaled_image, groups=(sprite_group, objects_group))


while True:
    frame_time = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")

    # draw the tiles
    tiles_group.draw(screen)
    animated_tiles_group.update(frame_time*3)
    animated_tiles_group.draw(screen)

    # draw the objects
    for sprite in sorted(objects_group, key=lambda sprite: sprite.rect.centery):
        screen.blit(sprite.image, sprite.rect.topleft)

    pygame.display.update()