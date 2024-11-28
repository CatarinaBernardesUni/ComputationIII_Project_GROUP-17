from background import background_setup
from enemy import Enemy
from config import *
import pygame
from player import Player
from shed import battle_area
from pytmx.util_pygame import load_pygame

def game_loop():
    # creating the player for the game - only done once :)
    player = Player()

    # by default, I start the game in the main area
    current_state = "main"

    # "endeless" game loop:
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "battle_area":
            current_state = battle_area(player)

def execute_game(player):
    # using the clock to control the time frame.
    clock = pygame.time.Clock()
    # screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width//2, height//2))

    ############################### MAP ################################

    tmx_data = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")
    (background_sprite_group, tiles_group, animated_tiles_group,
     objects_group, collision_sprites, battle_area_rect) = background_setup(tmx_data)

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

        display.fill("black")

        # Calculate camera offset
        camera_x = player.rect.centerx - display.get_width() // 2
        camera_y = player.rect.centery - display.get_height() // 2

        # Clamp the camera within the map boundaries
        camera_x = max(0, min(camera_x, width - display.get_width()))
        camera_y = max(0, min(camera_y, height - display.get_height()))

        camera_offset = pygame.Vector2(-camera_x, -camera_y)

        # draw the tiles
        # tiles_group.draw(display)
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)
        animated_tiles_group.update(frame_time * 3)
        # animated_tiles_group.draw(display)
        for animated_tile in animated_tiles_group:
            display.blit(animated_tile.image, animated_tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement



        # updating the player group
        player_group.update(collision_sprites)

        # checking if the player moved off-screen from the right to the left area
        # if player.rect.right >= width:
            # return "shed"

        # checking if the player is in the battle area
        if battle_area_rect.colliderect(player.rect):
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

            # updating the bullets group
            bullets.update()
            enemies.update(player)

            # Testing at home: player becomes red when colliding with an enemy # this display was screen
            if player.rect.colliderect(enemy.rect):
                pygame.draw.rect(display, red, player.rect)

            # enemies.draw(display)
            for enemy in enemies:
                display.blit(enemy.image, enemy.rect.topleft + camera_offset)

            # drawing the bullet sprites # this display was also screen
            for bullet in bullets:
                # bullet.draw(display)
                pygame.draw.circle(
                    display,
                    bullet.color,
                    (bullet.rect.centerx + camera_offset.x, bullet.rect.centery + camera_offset.y),
                    bullet.radius
                )

            # checking for collisions between player bullets and enemies
            for bullet in bullets:
                # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
                collided_enemies = pygame.sprite.spritecollide(bullet, enemies,
                                                               False)  # False means not kill upon impact
                for enemy in collided_enemies:
                    enemy.health -= 5

                    # removing the bullet from the screen after hitting the player
                    bullet.kill()

                    if enemy.health <= 0:
                        enemy.kill()

        # drawing the player and enemies sprites on the screen # these 2 displays were screen
        # player_group.draw(display)
        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        screen.blit(pygame.transform.scale(display, resolution), (0, 0)) # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    pygame.quit()