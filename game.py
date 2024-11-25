from enemy import Enemy
from config import *
import pygame
from player import Player
from shed import shed
from pytmx.util_pygame import load_pygame
from tile import Tile

def game_loop():
    # creating the player for the game - only done once :)
    player = Player()

    # by default I start the game in the main area
    current_state = "main"

    # "endeless" game loop:
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)

def execute_game(player):
    # using the clock to control the time frame.
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)

    ############################### MAP ################################
    tmx_data = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")

    # sprite groups for the objects and tiles
    sprite_group = pygame.sprite.Group()
    objects_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    animated_tiles_group = pygame.sprite.Group()

    # static tiles
    for layer in tmx_data.layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * 16, y * 16)
                Tile(position=pos, surf=surface, groups=(sprite_group, tiles_group))

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
                        pos = (x * 16, y * 16)
                        Tile(position=pos, surf=animation_frames[0], groups=(sprite_group, animated_tiles_group),
                             frames_animation=animation_frames, animation_duration=total_duration)

    for obj in tmx_data.objects:
        if obj.image:
            scaled_image = pygame.transform.scale(obj.image, (obj.width, obj.height))
            pos = (obj.x, obj.y)
            Tile(position=pos, surf=scaled_image, groups=(sprite_group, objects_group))
    ####################################################################

    # creating an empty group for the player (that was received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)
    # creating an empty bullet group that will be given as input to the player.shoot() method
    bullets = pygame.sprite.Group()
    # creating an enemy group
    enemies = pygame.sprite.Group()
    # before starting our main loop, set up the enemy cooldown
    enemy_cooldown = 0

    ###################################### MAIN GAME LOOP #######################################
    running = True
    while running:
        # controlling the frame rate
        frame_time = clock.tick(fps)

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill("black")

        # draw the tiles
        tiles_group.draw(screen)
        animated_tiles_group.update(frame_time * 3)
        animated_tiles_group.draw(screen)

        # draw the objects
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            screen.blit(sprite.image, sprite.rect.topleft)
        # automatically shoot bullets from the player
        player.shoot(bullets)

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # todo: creating more types of enemies
            enemy = Enemy()
            # adding the enemy to the group
            enemies.add(enemy)

            # in bullets, we use fps to spawn every second. Here we double that, to spawn every two seconds
            enemy_cooldown = fps * 2

        # updating the enemy cooldown
        enemy_cooldown -= 1

        # updating positions and visuals
        player_group.update()

        # updating the bullets group
        bullets.update()
        enemies.update(player)

        # checking if the player moved off-screen from the right to the left area
        if player.rect.right >= width:
            return "shed"


        # drawing the player and enemies sprites on the screen # these 2 displays were screen
        player_group.draw(screen)
        enemies.draw(screen)

        # drawing the bullet sprites # this display was also screen
        for bullet in bullets:
            bullet.draw(screen)

        # checking for collisions between player bullets and enemies
        for bullet in bullets:
            # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False) # False means not kill upon impact
            for enemy in collided_enemies:
                enemy.health -= 5

                # removing the bullet from the screen after hitting the player
                bullet.kill()

                if enemy.health <= 0:
                    enemy.kill()

        # Testing at home: player becomes red when colliding with an enemy # this display was screen
        if player.rect.colliderect(enemy.rect):
            pygame.draw.rect(screen, red, player.rect)

        # Testing at home: making the screen "move"
        # screen.blit(pygame.transform.scale(display, resolution), (0, 0)) # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    pygame.quit()