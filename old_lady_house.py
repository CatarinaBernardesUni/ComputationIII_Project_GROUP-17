from config import *
from collision import CollisionObject
from pytmx.util_pygame import load_pygame
from tile import Tile


def old_lady_house_setup(tmx_data_old_lady):
    background_sprite_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    objects_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    old_lady_house_exit_rect = None

    for layer in tmx_data_old_lady.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(position=pos, surf=surface, groups=(background_sprite_group, tiles_group))

    for obj in tmx_data_old_lady.objects:
        if obj.image:  # no rectangles are entering here because they do not have images
            scaled_image = pygame.transform.scale(obj.image, (obj.width, obj.height))
            pos = (obj.x, obj.y)
            Tile(position=pos, surf=scaled_image, groups=(background_sprite_group, objects_group))
        if obj in tmx_data_old_lady.get_layer_by_name("collisions on house"):
            CollisionObject(position=(obj.x, obj.y), size=(obj.width, obj.height), groups=(background_sprite_group,
                                                                                           collision_sprites))
        if obj in tmx_data_old_lady.get_layer_by_name("house exit"):
            old_lady_house_exit_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    return (background_sprite_group, tiles_group, objects_group,
            collision_sprites, old_lady_house_exit_rect)


def old_lady_house_area(player):
    clock = pygame.time.Clock()
    home_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    tmx_data_old_lady_house = load_pygame("data/WE OLD LADY HOUSE/WE OLD LADY HOUSE MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, old_lady_house_exit_rect) = old_lady_house_setup(tmx_data_old_lady_house)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (111, 265)
    player.state = "up"
    ###################################### MAIN GAME LOOP #######################################
    running = True
    while running:
        # controlling the frame rate
        frame_time = clock.tick(fps)

        # handling events:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()

        ############################### CAMERA - REPEATED CODE ################################
        # Calculate camera offset
        camera_x = player.rect.centerx - display.get_width() // 2
        camera_y = player.rect.centery - display.get_height() // 2

        # Clamp the camera within the map boundaries
        camera_x = max(0, min(camera_x, width - display.get_width()))
        camera_y = max(0, min(camera_y, height - display.get_height()))

        camera_offset = pygame.Vector2(-camera_x, -camera_y)
        ####################################################################################

        # draw the tiles
        # tiles_group.draw(display)
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group
        player_group.update(collision_sprites, display)

        if old_lady_house_exit_rect and old_lady_house_exit_rect.colliderect(player.rect):
            player.just_left_old_lady_house = True
            return "main"

        # display.blit(player_score_surf, player_score_rect)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        home_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left
        display.fill("black")

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()
