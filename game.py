from config import *
import pygame
from player import Player
from enemy import Enemy
from shed import shed
import interface


def game_over():
    screen.blit(game_over_image, (0, 0))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 157 <= mouse[0] <= 340 and 505 <= mouse[1] <= 598:
                    game_loop()
                    waiting = False

                if 282 <= mouse[0] <= 431 and 502 <= mouse[1] <= 535:
                    pygame.quit()
                    exit()


def game_loop():
    # creating the player for the game, it is only defined once
    player = Player()

    # by default, I start the game inn the main area
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

    background = pygame.image.load("images/screens/stardew_valley.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Testing at home: making the display "smaller" than the background
    # display = pygame.Surface((width // 2, height // 2))

    # using the clock to control the time frame
    clock = pygame.time.Clock()

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

    while True:
        # controlling the frame rate
        clock.tick(fps)

        # setting up the background # change to display later
        screen.blit(background, (0, 0))  # 0,0 will fill the entire screen

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
        enemy_hurt = pygame.image.load("images/monsters/monster 1/enemy_hurt.png")
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

        # Testing at home: player becomes red when colliding with an enemy # this display was screen
        # the problem with this part of the code is that the health is decreasing very fast
        def remove_health():
            player.health.__delitem__(-1)  # B  deletes the last item in the list of hearts

        if player.rect.colliderect(enemy.rect):
            # player.image = pygame.transform.scale(player_img1, player_size)
            # pygame.draw.rect(screen, red, player.rect)
            if not player.health:
                game_over()
                #    clock.tick(1)

            if pygame.time.get_ticks() - player.damage_cooldown > player.cooldown_duration:
                # aqui falta mostrar os corações na tela (I print the health to see if it's working)
                remove_health()
                player.damage_cooldown = pygame.time.get_ticks()
                print(player.health)

        # Testing at home: making the screen "move"
        # screen.blit(pygame.transform.scale(display, resolution), (0, 0)) # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    pygame.quit()

    pygame.display.update()
    clock.tick(15)
