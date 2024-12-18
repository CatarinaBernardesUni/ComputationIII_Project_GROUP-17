from dog import Dog
from background import background_setup
#from power_up import PowerUp
from cave import cave_area
from home import home_area
from player import *
from enemy import Enemy, enemies_data
import interface
from progress import *
from config import *
from pytmx.util_pygame import load_pygame
from store import inside_store
from utils import paused, calculate_camera_offset
from old_lady_house import old_lady_house_area
from wave import WaveManager
from weapon import *
from mouse_position import get_mouse_position, draw_button
from inventory import inventory_menu


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
                if 384 <= mouse[0] <= 626 and 489 <= mouse[1] <= 580:
                    info['health'] = 5
                    game_loop()
                    waiting = False

                if 690 <= mouse[0] <= 935 and 487 <= mouse[1] <= 582:
                    progress()
                    pygame.quit()
                    exit()
                if 531 <= mouse[0] <= 771 and 608 <= mouse[1] <= 700:
                    interface.interface()
                    waiting = False


def game_loop():
    # by default, I start the game in the main area
    current_state = "main"
    # creating the player for the game, it is only defined once
    player = Player()
    dog = Dog(player)

    # endeless game loop
    while True:
        if current_state == "main":
            current_state = execute_game(player, dog)
        elif current_state == "cave":
            current_state = cave_area(player)
        elif current_state == "home":
            current_state = home_area(player)
        elif current_state == "old lady house":
            current_state = old_lady_house_area(player)
        elif current_state == "store":
            current_state = inside_store(player)
        elif current_state == "game_over":
            game_over()

def execute_game(player, dog):
    # SETUP
    # using the clock to control the time frame.
    clock = pygame.time.Clock()
    # screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2, height // 2))
    in_battle_area = False

    ############################### MAP ################################

    tmx_data = load_pygame("data/WE GAME MAP/WE GAME MAP.tmx")
    (background_sprite_group, tiles_group, animated_tiles_group,
     objects_group, collision_sprites, battle_area_rect, store_rect, cave_entrance_rect, home_rect, old_lady_house_rect) = background_setup(tmx_data)

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
    # fire_sword = Sword(player, weapon_group, "fire_sword")
    # dagger = Sword(player, weapon_group, "dagger")
    # winter_sword = Sword(player, weapon_group, "winter_sword")

    # ghost_bow = Bow(player, weapon_group, "ghost_bow")
    # ice_bow = Bow(player, weapon_group, "ice_bow")
    # light_bow = Bow(player, weapon_group, "light_bow")

    # gold_axe = Axe(player, weapon_group, "gold_axe")
    # ruby_axe = Axe(player, weapon_group, "ruby_axe")

    # creating an instance of the wave (it is only going to start once the player enters the battle area)
    wave_manager = WaveManager(player, enemies_data, battle_area_rect)

    # starting the first wave
    wave_manager.start_next_wave()

    event_display_start_wave_message = pygame.USEREVENT + 0
    ###################################### MAIN GAME LOOP #######################################
    running = True
    while running:
        # controlling the frame rate
        frame_time = clock.tick(fps)

        mouse_pos = pygame.mouse.get_pos()
        scaled_mouse_pos = (mouse_pos[0]//2, mouse_pos[1]//2)

        ################################ Calculate camera offset  #######################
        camera_offset = calculate_camera_offset(player, display)
        ###################################################################################

        # draw the tiles
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)
        animated_tiles_group.update(frame_time * 3)

        for animated_tile in animated_tiles_group:
            display.blit(animated_tile.image, animated_tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group and dog
        # so dog can appear on screen when bought
        player_group.update(collision_sprites, display, frame_time, battle_area_rect)

        if player.dog.bought:
            if player.dog not in player_group:
                player_group.add(player.dog)
            player.dog.follow_player()

        # checking if the player entered the cave
        if cave_entrance_rect and cave_entrance_rect.colliderect(player.rect):
            return "cave"

        if player.just_left_cave:
            #player.rect.x -= 135
            #player.rect.y += 155
            player.rect.center = (510, 445)
            player.just_left_cave = False

        # display.blit(player_score_surf, player_score_rect)

        # checking if player enters the store are
        if store_rect and store_rect.colliderect(player.rect):
            return "store"

        if player.just_left_store:
            player.rect.center = (500, 240)
            player.state = "down"
            player.just_left_store = False

        # make the player able to go inside the home
        if home_rect and home_rect.colliderect(player.rect):
            return "home"
        if player.just_left_home:
            player.rect.center = (1150, 150)
            player.just_left_home = False

        # player in the old lady house
        if old_lady_house_rect and old_lady_house_rect.colliderect(player.rect):
            return "old lady house"
        if player.just_left_old_lady_house:
            player.rect.center = (325, 170)
            player.just_left_old_lady_house = False

        # checking if the player is in the battle area
        if battle_area_rect.colliderect(player.rect):
            # initiating the battle area music:
            if not in_battle_area:
                in_battle_area = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/TheGreatBattle.mp3")
                pygame.mixer.music.play(-1)

            player.active_weapon_group.update(frame_time)
            for weapon in player.active_weapon_group:
                display.blit(weapon.image, weapon.rect.topleft + camera_offset)

            if not wave_manager.is_wave_active and not player.is_leaving_battle:
                wave_manager.activate_wave()

            wave_manager.update(display, frame_time, enemy_cooldown)

            # drawing the bullet sprites # this display was also screen
            #for bullet in bullets:
                # bullet.draw(display)
                #pygame.draw.circle(
                    #display,
                    #bullet.color,
                    #(bullet.rect.centerx + camera_offset.x, bullet.rect.centery + camera_offset.y),
                    #bullet.radius
                #)
            # checking for collisions between player bullets and enemies
            # for bullet in bullets:
                # todo: one type of bullet might be strong enough to kill on impact and the value of dokill will be True
                # collided_enemies = pygame.sprite.spritecollide(bullet, enemies,
                                                               # True)  # True means kill upon impact

            if info['health'] <= 0:
                game_over()

        # leaves battle area and music returns to normal game one
        else:
            if in_battle_area:
                # Player has left the battle area
                in_battle_area = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/Adventure.mp3")
                pygame.mixer.music.play(-1)

        # drawing the player and enemies sprites on the screen # these 2 displays were screen
        # player_group.draw(display)
        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # drawing the inventory button
        inventory_button = draw_button(display, 550, y=10, width=70, height=35,
                                       text="Inventory",
                                       text_color=brick_color, image_path="images/buttons/basic_button.png",
                                       font=cutefont)

        # handling events:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused()
                if event.key == pygame.K_ESCAPE:
                    inventory_menu(player)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if inventory_button.collidepoint(scaled_mouse_pos):
                    inventory_menu(player)

        # updating the display
        screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()

    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()
