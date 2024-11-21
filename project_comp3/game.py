from config import *
import pygame
from player import Player
from enemy import Enemy
from shed import shed


def game_loop():
    # creating the player for the game - only done once!!!
    player = Player()

    # by default I start the game in the main area
    current_state = "main"

    # (endless) game loop:
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)


def execute_game(player):

    # SETUP:

    # setting up the background
    background = pygame.image.load("images/Farm.jpg")
    background = pygame.transform.scale(background, (width, height))

    # using the clock to control the time frame
    clock = pygame.time.Clock()

    # screen setup:
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # creating an empty group for the player (that we received as input)
    player_group = pygame.sprite.Group()
    # adding the player to the group
    player_group.add(player)

    # creating an empty bullet group that will be given as input to the player.shoot() method
    bullets = pygame.sprite.Group()

    # creating the enemy group
    enemies = pygame.sprite.Group()

    # before starting our main loop, setup the enemy cooldown variable
    enemy_cooldown = 0

    # MAIN GAME LOOP

    running = True

    while running:

        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0))  # 0,0 fills the entire screen

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # automatically shoot bullets from the player
        player.shoot(bullets)

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # creating an enemy... would be so cool if there were more than one type ... oh well...
            enemy = Enemy()

            # adding the enemy to the group
            enemies.add(enemy)

            # in bullets, we use fps to spawn every second. Here we double that, to spaw every two seconds
            enemy_cooldown = fps * 2

        # updating the enemy cooldown
        enemy_cooldown -= 1

        # updating positions and visuals:
        # calling the .update() method to all the instances in the player group
        player_group.update()

        # updating the bullets and enemy group
        bullets.update()
        enemies.update(player)

        # checking if the player moved off-screen from the right to the next area
        if player.rect.right >= width:
            return "shed"

        # drawing the player and enemies sprites on the screen:
        player_group.draw(screen)
        enemies.draw(screen)

        # drawing the bullet sprites:
        for bullet in bullets:
            bullet.draw(screen)

        # checking for collisions between player bullets and enemies
        for bullet in bullets:
            # getting the enemies that were hit by a bullet
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)

            for enemy in collided_enemies:

                # every hit enemy needs to lose life... wink wink: different enemies should have different healths
                # todo: create damage parameter
                # every bullet hit will reduce the life by 5 hp
                enemy.health -= 5

                # removing the bullet from the screen (as it's lodged in the enemy's heart)
                bullet.kill()

                # checking if enemy is dead
                if enemy.health <= 0:
                    enemy.kill()


        pygame.display.flip()
