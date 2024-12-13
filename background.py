import pygame
from config import *
from tile import Tile
from collision import CollisionObject
#from store import inside_store
#from player import Player


def background_setup(tmx_data):
    # sprite groups for the objects and tiles
    # the background sprite group is a container for all the background sprites in the game
    background_sprite_group = pygame.sprite.Group()

    tiles_group = pygame.sprite.Group()
    animated_tiles_group = pygame.sprite.Group()
    # although the rectangles being used for collisions are also objects, they are not included in this group
    objects_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    # storing the rect of the "battle area" and "store"
    battle_area_rect = None
    store_rect = None
    cave_entrance_rect = None
    home_rect = None
    old_lady_house_rect = None

    # static tiles
    for layer in tmx_data.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(position=pos, surf=surface, groups=(background_sprite_group, tiles_group))

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
                        pos = (x * tile_size, y * tile_size)
                        Tile(position=pos, surf=animation_frames[0], groups=(background_sprite_group,
                                                                             animated_tiles_group),
                             frames_animation=animation_frames, animation_duration=total_duration)

    # objects
    for obj in tmx_data.objects:
        if obj.image:  # no rectangles are entering here because they do not have images
            scaled_image = pygame.transform.scale(obj.image, (obj.width, obj.height))
            pos = (obj.x, obj.y)
            Tile(position=pos, surf=scaled_image, groups=(background_sprite_group, objects_group))
        if obj in tmx_data.get_layer_by_name("COLLISIONS"):
            CollisionObject(position=(obj.x, obj.y), size=(obj.width, obj.height), groups=(background_sprite_group,
                                                                                           collision_sprites))
        if obj in tmx_data.get_layer_by_name("FIGHT AREA"):
            battle_area_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        if obj in tmx_data.get_layer_by_name("Flower Roof House"):
            store_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        if obj in tmx_data.get_layer_by_name("Cave"):
            cave_entrance_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        if obj in tmx_data.get_layer_by_name("Blue Roof House"):
            home_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        if obj in tmx_data.get_layer_by_name("Purple Roof House"):
            old_lady_house_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    return (background_sprite_group, tiles_group, animated_tiles_group, objects_group,
            collision_sprites, battle_area_rect, store_rect, cave_entrance_rect, home_rect, old_lady_house_rect)
