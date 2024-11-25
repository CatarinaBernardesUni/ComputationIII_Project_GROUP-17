import pygame
import sys
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z_order=0):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z_order = z_order

pygame.init()
screen = pygame.display.set_mode((1280, 720))
tmx_data = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")
sprite_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

scale_factor = 1
for layer in tmx_data.layers:
    if hasattr(layer, "data"):
        for x, y, surface in layer.tiles():
            pos = (x * 16, y * 16)
            Tile(pos=pos, surface=surface, groups=(sprite_group, tiles_group))

for obj in tmx_data.objects:
    if obj.image:
        # Scale the image if necessary
        scaled_image = pygame.transform.scale(obj.image, (int(obj.width * scale_factor), int(obj.height * scale_factor)))
        # Rotate the image if necessary
        pos = (obj.x, obj.y)  # Adjust if the origin is not top-left
        Tile(pos=pos, surface=scaled_image, groups=(sprite_group, objects_group))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")

    # draw the tiles
    tiles_group.draw(screen)
    # draw the objects
    for sprite in sorted(objects_group, key=lambda sprite: sprite.rect.centery):
        screen.blit(sprite.image, sprite.rect.topleft)

    pygame.display.update()