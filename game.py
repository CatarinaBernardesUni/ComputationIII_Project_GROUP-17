from config import *
from player import Player
from enemy import Enemy
# from shed import shed
from pytmx.util_pygame import load_pygame
from tile import *
from groups import AllSprites

def execute_game():
    player = None
    # screen setup:
    screen = pygame.display.set_mode(resolution)
    #screen.fill('black')
    # using the clock to control the time frame
    clock = pygame.time.Clock()
    # groups
    all_sprites = AllSprites()
    collision_group = pygame.sprite.Group()

    ###################################### TILE MAP #######################################
    game_map = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")
    for x, y, image in game_map.get_layer_by_name("GROUND").tiles():
        Tile((x * tile_size, y * tile_size), image, all_sprites)
    for x, y, image in game_map.get_layer_by_name("PLANTS ABOVE GROUND").tiles():
        Tile((x * tile_size, y * tile_size), image, all_sprites)
    for x, y, image in game_map.get_layer_by_name("Plants above 2").tiles():
        Tile((x * tile_size, y * tile_size), image, all_sprites)
    for x, y, image in game_map.get_layer_by_name("Plants above 3").tiles():
        Tile((x * tile_size, y * tile_size), image, all_sprites)
    for x, y, image in game_map.get_layer_by_name("Plants above 4").tiles():
        Tile((x * tile_size, y * tile_size), image, all_sprites)
    for x, y, image in game_map.get_layer_by_name("Plants above 5").tiles():
        Tile((x * tile_size, y * tile_size), image, all_sprites)


    for obj in game_map.get_layer_by_name("Objects"): # todo: I don't want objects to be obstacles
        CollisionObject((obj.x, obj.y), obj.image, (all_sprites, collision_group))

    for obj in game_map.get_layer_by_name("COLLISIONS"):
        CollisionObject((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (all_sprites, collision_group))

    for obj in game_map.get_layer_by_name("Markers"):
        if obj.name == "Player":
            player = Player((obj.x, obj.y), all_sprites, collision_group)


    # creating an empty group for the player (that was received as input)
    #player_group = pygame.sprite.Group()
    # adding the player to the group
    #player_group.add(player)
    # creating an empty bullet group that will be given as input to the player.shoot() method
    #bullets = pygame.sprite.Group()
    # creating an enemy group
    #enemies = pygame.sprite.Group()
    # before starting our main loop, set up the enemy cooldown
    #enemy_cooldown = 0

    ###################################### MAIN GAME LOOP #######################################
    running = True
    while running:
        # controlling the frame rate
        clock.tick(fps)

        # handling events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        all_sprites.update()

        all_sprites.drawing(player.rect.center)
        all_sprites.draw(screen)
        # automatically shoot bullets from the player
        #player.shoot(bullets)

        # spawning enemies every two seconds
        #if enemy_cooldown <= 0:
            # todo: creating more types of enemies
            #enemy = Enemy()

            # adding the enemy to the group
            #enemies.add(enemy)

            # in bullets, we use fps to spawn every second. Here we double that, to spawn every two seconds
            #enemy_cooldown = fps * 2

        # updating the enemy cooldown
        #enemy_cooldown -= 1

        # updating positions and visuals
        #player_group.update()

        # updating the bullets group
        #bullets.update()
        #enemies.update(player)

        # checking if the player moved off-screen from the right to the left area
        #if player.rect.right >= width:
            #return "shed"


        # drawing the player and enemies sprites on the screen # these 2 displays were screen
        #player_group.draw(screen)
        #enemies.draw(screen)
        #all_sprites.drawing(player.rect.center)

        # drawing the bullet sprites # this display was also screen
        #for bullet in bullets:
            #bullet.draw(screen)

        # checking for collisions between player bullets and enemies
        #for bullet in bullets:
            # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
            #collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False) # False means not kill upon impact
            #for enemy in collided_enemies:
                #enemy.health -= 5

                # removing the bullet from the screen after hitting the player
                #bullet.kill()

                #if enemy.health <= 0:
                    #enemy.kill()

        # Testing at home: player becomes red when colliding with an enemy # this display was screen
        #if player.rect.colliderect(enemy.rect):
            #pygame.draw.rect(screen, red, player.rect)

        # Testing at home: making the screen "move"
        # screen.blit(pygame.transform.scale(display, resolution), (0, 0)) # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    pygame.quit()