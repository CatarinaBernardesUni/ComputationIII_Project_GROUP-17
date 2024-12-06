from background import background_setup
import pygame

from cave import cave_area
from player import *
from enemy import Enemy
import interface
from progress import *
from config import *
from pytmx.util_pygame import load_pygame
from store import inside_store
from weapon import Weapon


def choose_character():
    screen.blit(choose_character_image, (0, 0))

    while True:
        for ev in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if ev.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 243 <= mouse[0] <= 547 and 222 <= mouse[1] <= 527:
                    config.character_choice = "player 1"
                    game_loop()
                if 720 <= mouse[0] <= 1023 and 226 <= mouse[1] <= 526:
                    config.character_choice = "player 2"
                    game_loop()

        pygame.display.update()


def game_over():
    screen.blit(game_over_image, (0, 0))
    pygame.display.update()
    # player = Player()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 157 <= mouse[0] <= 340 and 505 <= mouse[1] <= 598:
                    info['health'] = 5
                    game_loop()
                    waiting = False

                if 282 <= mouse[0] <= 431 and 502 <= mouse[1] <= 535:
                    progress()
                    pygame.quit()
                    exit()
                if 27 <= mouse[0] <= 273 and 187 <= mouse[1] <= 429:
                    interface.interface()
                    waiting = False


def paused():
    pause = True
    while pause:
        screen.blit(pause_image, (0, 0)) # todo: change the amount of different variables called screen
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 443 <= mouse[0] <= 610 and 112 <= mouse[1] <= 169:
                    interface.interface()
                if 637 <= mouse[0] <= 802 and 112 <= mouse[1] <= 171:
                    pause = False
        pygame.display.update()


def game_loop():
    # by default, I start the game in the main area
    current_state = "main"
    # creating the player for the game, it is only defined once
    player = Player()

    # endeless game loop
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "cave":
            current_state = cave_area(player)

def execute_game(player):
    # SETUP
    global player_score_surf, player_score_rect
    # using the clock to control the time frame.
    clock = pygame.time.Clock()
    # screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2, height // 2))

    ############################### MAP ################################

    tmx_data = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")
    (background_sprite_group, tiles_group, animated_tiles_group,
     objects_group, collision_sprites, battle_area_rect, store_rect, cave_entrance_rect) = background_setup(tmx_data)

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

    weapon_group = pygame.sprite.Group()
    fire_sword = Weapon(player, "Flaming Sword", 10, 10, 10, 10, 10,
                        10, 10, weapon_group)

    ###################################### MAIN GAME LOOP #######################################
    running = True
    while running:
        # controlling the frame rate
        frame_time = clock.tick(fps)

        # mouse = pygame.mouse.get_pos()
        # handling events:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if keys[pygame.K_SPACE]:
                paused()

        # display.fill("black")

        ################################ Calculate camera offset  #######################
        camera_x = player.rect.centerx - display.get_width() // 2
        camera_y = player.rect.centery - display.get_height() // 2

        # Clamp the camera within the map boundaries
        camera_x = max(0, min(camera_x, width - display.get_width()))
        camera_y = max(0, min(camera_y, height - display.get_height()))

        camera_offset = pygame.Vector2(-camera_x, -camera_y)
        ###################################################################################

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
        player_group.update(collision_sprites, display)

        # checking if the player moved off-screen from the right to the left area
        # if player.rect.right >= width:
        # return "shed"

        weapon_group.update(frame_time)

        # checking if the player entered the cave
        if cave_entrance_rect and cave_entrance_rect.colliderect(player.rect):
            return "cave"

        if player.just_left_cave:
            player.rect.x -= 90
            player.rect.y += 105
            player.just_left_cave = False

        display.blit(player_score_surf, player_score_rect)

        # checking if player enters the store are
        if store_rect and store_rect.colliderect(player.rect):
            inside_store(player)
            # todo: is the store being drawn on top of the background?
            # when player leaves the house it goes here
            player.rect.x = player.rect.x
            player.rect.y = player.rect.y + 20

        # checking if the player is in the battle area
        if battle_area_rect.colliderect(player.rect):
            # automatically shoot bullets from the player
            player.shoot(bullets)
            # spawning enemies every two seconds
            if enemy_cooldown <= 0:
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
            # todo: put this back
            # weapon_group.update()

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
            # drawing the weapons
            # todo: put this back too
            # for weapon in weapon_group:
                # display.blit(weapon.image, weapon.rect.topleft + camera_offset)

            enemy_hurt = pygame.image.load("images/monsters/monster 3/enemy_hurt.png")

            # checking for collisions between player bullets and enemies
            for bullet in bullets:
                # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
                collided_enemies = pygame.sprite.spritecollide(bullet, enemies,
                                                               False)  # False means not kill upon impact
                for enemy in collided_enemies:
                    enemy.image = pygame.transform.scale(enemy_hurt, enemy_size)
                    enemy.health -= 5

                    # removing the bullet from the screen after hitting the player
                    bullet.kill()

            if enemy.health <= 0:
                enemy.kill()
                info['score'] += 1
                player_score_surf = pixel.render(f"score: {info['score']}", True, "black")
                player_score_rect = player_score_surf.get_rect(center=(80, 80))

            if player.rect.colliderect(enemy.rect):
                # pygame.draw.rect(screen, red, player.rect)
                if info['health'] <= 0:
                    game_over()

            # this "if" sees if the difference between the time the player is hit and the last time the
            # player was hit is bigger than the time it needs to cooldown
            if pygame.time.get_ticks() - player.damage_cooldown > player.cooldown_duration:
                # here is missing showing hearts as health (I print the health to see if it's working)
                remove_health()
                player.damage_cooldown = pygame.time.get_ticks()  # and here sets the "last time it was hit"

        # drawing the player and enemies sprites on the screen # these 2 displays were screen
        # player_group.draw(display)
        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        for weapon in weapon_group:
            display.blit(weapon.image, weapon.rect.topleft + camera_offset)

        screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()

    # pygame.display.update()
    # clock.tick(15)
