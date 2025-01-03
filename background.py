from config import *
from tile import Tile
from collision import CollisionObject


def background_setup(tmx_data):
    """
    Sets up the game's background, including tiles, animated tiles, objects, and collision areas.

    Parameters
    ----------
    tmx_data : TiledMap (a .tmx file)
        The Tiled map data containing information about layers, tiles, and objects.

    Returns
    -------
    tuple
        A tuple containing the following:
        - background_sprite_group : pygame.sprite.Group
            A group containing all background sprites.
        - tiles_group : pygame.sprite.Group
            A group containing all static tiles.
        - animated_tiles_group : pygame.sprite.Group
            A group containing animated tiles.
        - objects_group : pygame.sprite.Group
            A group containing objects with images.
        - collision_sprites : pygame.sprite.Group
            A group containing collision objects.
        - battle_area_rect : pygame.Rect or None
            A rectangle defining the battle area, or None if not defined.
        - store_rect : pygame.Rect or None
            A rectangle defining the store area, or None if not defined.
        - cave_entrance_rect : pygame.Rect or None
            A rectangle defining the cave entrance, or None if not defined.
        - home_rect : pygame.Rect or None
            A rectangle defining the player's home, or None if not defined.
        - old_lady_house_rect : pygame.Rect or None
            A rectangle defining the old lady's house, or None if not defined.
        - pink_house_rect : pygame.Rect or None
            A rectangle defining the pink house, or None if not defined.
        - shed_rect : pygame.Rect or None
            A rectangle defining the shed, or None if not defined.
        - greenhouse_rect : pygame.Rect or None
            A rectangle defining the greenhouse, or None if not defined.
    """
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
    pink_house_rect = None
    shed_rect = None
    greenhouse_rect = None

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

        if obj in tmx_data.get_layer_by_name("Pink Roof House"):
            pink_house_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        if obj in tmx_data.get_layer_by_name("Yellow Roof House"):
            shed_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        if obj in tmx_data.get_layer_by_name("Greenhouse"):
            greenhouse_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    return (background_sprite_group, tiles_group, animated_tiles_group, objects_group,
            collision_sprites, battle_area_rect, store_rect, cave_entrance_rect, home_rect, old_lady_house_rect,
            pink_house_rect, shed_rect, greenhouse_rect)
