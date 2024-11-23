from config import *
import pygame
from player import Player
from enemy import Enemy
from shed import shed
from pytmx.util_pygame import load_pygame

from tile import Tile


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
    background = pygame.image.load("images/stardew_valley.jpg")
    background = pygame.transform.scale(background, (width, height))
    tmx_data = load_pygame("...") # todo: add the path to the tmx file
    tile_group = pygame.sprite.Group()

    # cycle through all visible layers in the tmx file
    for layer in tmx_data.visible_layers:
        # layer as the attribute data which objects don't have
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * tile_size, y * tile_size)
                Tile(pos=pos, surface=surface, groups=tile_group)

    for obj in tmx_data.objects:
        pos = obj.x, obj.y  # this is not a tile set which means that the x and y are information
                            # that we can use straight away
        if obj.image:
            Tile(pos=pos, surface=obj.image, groups=tile_group)

    # Testing at home: making the display "smaller" than the background
    # display = pygame.Surface((width // 2, height // 2))

    # using the clock to control the time frame
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)

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

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Testing at home: loading the map code
        #tile_rects = []
        #y = 0
        #for row in game_map:
        #    x = 0
        #    for tile in row:
        #        if tile == 1:
        #            display.blit(wall, (x * tile_size, y * tile_size)) # we are multiplying it to get the pixel
        #                                                                    # coordinates of the tile
        #        if tile == 2:
        #            display.blit(floor, (x * tile_size, y * tile_size))

        #        if tile == 0:
        #            tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)) #these tile sizes
        #                                                                                            # are assuming that width and height are the same
        #        x += 1
        #    y += 1

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

        # drawing the tiles
        tile_group.draw(screen)

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