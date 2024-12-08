from collision import CollisionObject
from config import *
from pytmx.util_pygame import load_pygame

# from game import paused
from tile import Tile


def home_setup(tmx_data_home):
    background_sprite_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    objects_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    home_exit_rect = None

    # static tiles
    for layer in tmx_data_home.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(position=pos, surf=surface, groups=(background_sprite_group, tiles_group))

    # objects
    for obj in tmx_data_home.objects:
        if obj.image:  # no rectangles are entering here because they do not have images
            scaled_image = pygame.transform.scale(obj.image, (obj.width, obj.height))
            pos = (obj.x, obj.y)
            Tile(position=pos, surf=scaled_image, groups=(background_sprite_group, objects_group))
        if obj in tmx_data_home.get_layer_by_name("collisions on home"):
            CollisionObject(position=(obj.x, obj.y), size=(obj.width, obj.height), groups=(background_sprite_group,
                                                                                           collision_sprites))
        if obj in tmx_data_home.get_layer_by_name("home exit"):
            home_exit_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    return (background_sprite_group, tiles_group, objects_group,
            collision_sprites, home_exit_rect)

def home_area(player):
    clock = pygame.time.Clock()
    home_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    ############################### HOUSE MAP ################################

    tmx_data_home = load_pygame("data/WE HOME/WE HOME MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, home_exit_rect) = home_setup(tmx_data_home)

    ####################################################################

    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (385, 550)
    player.state = "down"

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
            # if keys[pygame.K_SPACE]:
                # paused() # todo: pause is giving circular import

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

        if home_exit_rect and home_exit_rect.colliderect(player.rect):
            player.just_left_home = True
            return "main"

        display.blit(player_score_surf, player_score_rect)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        home_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()
