from pytmx.util_pygame import load_pygame
import random
from utils import *
from mouse_position import draw_button


def old_lady_house_area(player):
    clock = pygame.time.Clock()
    home_screen = pygame.display.set_mode(resolution)
    display = pygame.Surface((width // 2.2, height // 2.2))

    tmx_data = load_pygame("data/WE OLD LADY HOUSE/WE OLD LADY HOUSE MAP.tmx")
    (background_sprite_group, tiles_group, objects_group,
     collision_sprites, exit_rect, speech_bubble_rect, clues_rect) = area_setup(tmx_data, "collisions on house",
                                                                                "house exit", "little easter egg",
                                                                                "old lady talks")
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # setting the player initial position on the home
    player.rect.center = (111, 253)
    player.state = "up"

    # these variables are for the speech bubble of the old lady
    # if I didn't do this code, she would keep spamming random speech bubbles
    # basically,
    current_speech = None
    player_colliding = False
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
            if keys[pygame.K_SPACE]:
                paused()

        ############################### CAMERA - REPEATED CODE ################################
        # Calculate camera offset
        camera_offset = calculate_camera_offset(player, display)
        ####################################################################################

        # draw the tiles
        # tiles_group.draw(display)
        for tile in tiles_group:
            display.blit(tile.image, tile.rect.topleft + camera_offset)

        # draw the objects in order of their y position
        for sprite in sorted(objects_group, key=lambda sprite_obj: sprite_obj.rect.centery):
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)  # camera offset added for movement

        # updating the player group
        player_group.update(collision_sprites, display, frame_time)

        if exit_rect and exit_rect.colliderect(player.rect):
            player.just_left_old_lady_house = True
            return "main"

        # To track whether the player is already colliding

        if speech_bubble_rect and speech_bubble_rect.colliderect(player.rect):
            if not player_colliding:  # checks if it's the first time colliding
                # this chooses a random speech from the list of speeches
                current_speech = random.choice(old_lady_speech)
                # current_speech = random.choice(old_lady_speech)
                player_colliding = True  # indicates if collision is happening
            # this "display.blit" is outside the "if not" to keep showing the same current_speech that was set when
            # the player first collided with the old lady
            draw_button(display, 170, 80, 150, 100,
                        current_speech, brick_color,
                        "images/dialogs/dialog box medium.png", cutefont)
            # display.blit(current_speech, (135, 40))
        else:
            # when the player stops colliding this is set to false so next time they collide the speech changes
            player_colliding = False

        # display.blit(player_score_surf, player_score_rect)
        if clues_rect and clues_rect.colliderect(player.rect):
            if info['stolen_grandma'] <= 0:
                draw_button(display, 10, 150, 320, 100,
                            "click  'E'  to  steal  gold  from  your  grandma!", brick_color,
                            "images/inventory/inventory_menu.png", cutefont)
                display.blit(gold_chest, (150, 150))
                if keys[pygame.K_e]:
                    coin_music.play()
                    info['stolen_grandma'] = 1
                    player.add_gold(150)
                    # this way the player can only open this chest once in the whole game
            else:
                draw_button(display, 10, 150, 320, 100,
                            "+ 150  gold   (already  claimed)", brick_color,
                            "images/inventory/inventory_menu.png", cutefont)

        for sprite in player_group:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # collision_sprites.draw(display)
        for sprite in collision_sprites:
            display.blit(sprite.image, sprite.rect.topleft + camera_offset)

        home_screen.blit(pygame.transform.scale(display, resolution), (0, 0))  # 0,0 being the top left
        display.fill("black")

        # updates the whole screen since the frame was last drawn
        pygame.display.flip()
        # clock.tick(fps)
    # the main while loop was terminated
    progress()
    pygame.quit()
    exit()
