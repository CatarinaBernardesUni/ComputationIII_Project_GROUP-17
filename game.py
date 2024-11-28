import pygame
from player import *
from enemy import Enemy
from shed import shed
import interface
from progress import *


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
        screen.blit(pause_image, (width // 2 - 375, height // 2 - 300))
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 295 <= mouse[0] <= 600 and 533 <= mouse[1] <= 631:
                    interface.interface()
                if 667 <= mouse[0] <= 976 and 533 <= mouse[1] <= 631:
                    pause = False
        pygame.display.update()


def game_loop():
    # creating the player for the game, it is only defined once
    player = Player()
    # by default, I start the game in the main area
    current_state = "main"

    # endeless game loop
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)


def execute_game(player):
    # SETUP
    # setting up the background

    global player_score_surf, player_score_rect
    background = pygame.image.load("images/screens/farm.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Testing at home: making the display "smaller" than the background
    # display = pygame.Surface((width // 2, height // 2))

    # using the clock to control the time frame

    # screen setup:
    # screen = pygame.display.set_mode(resolution)

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
        clock.tick(fps)

        # setting up the background # change to display later
        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen
        screen.blit(player_score_surf, player_score_rect)
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

        # Testing at home: loading the map code
        # tile_rects = []
        # y = 0
        # for row in game_map:
        #    x = 0
        #    for tile in row:
        #        if tile == 1:
        #            display.blit(wall, (x * tile_size, y * tile_size)) # we are multiplying it to get the pixel
        #                                                                    # coordinates of the tile
        #        if tile == 2:
        #            display.blit(floor, (x * tile_size, y * tile_size))

        # if tile == 0: tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)) #these
        # tile sizes # are assuming that width and height are the same x += 1 y += 1

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
        enemy_hurt = pygame.image.load("images/monsters/monster 3/enemy_hurt.png")
        # drawing the bullet sprites # this display was also screen
        for bullet in bullets:
            bullet.draw(screen)

        # checking for collisions between player bullets and enemies
        for bullet in bullets:
            # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)  # False means not kill upon impact
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

        # Testing at home: player becomes red when colliding with an enemy # this display was screen
        # the problem with this part of the code is that the health is decreasing very fast

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
                # to this time because he was hit

        # Testing at home: making the screen "move"
        # screen.blit(pygame.transform.scale(display, resolution), (0, 0)) # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()

    # pygame.display.update()
    # clock.tick(15)
