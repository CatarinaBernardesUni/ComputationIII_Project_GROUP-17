import random
import os

import pygame.time

from config import *

from enemy import Enemy
from player import remove_health
from utils import calculate_camera_offset

class WaveManager:
    def __init__(self, player, enemies_data, battle_area_rect):

        self.battle_area_rect = battle_area_rect
        self.enemies_data = enemies_data
        self.player = player
        self.active_enemies = pygame.sprite.Group()
        self.current_wave = 0
        self.enemies_defeated = 0
        self.total_enemies = 0
        self.is_wave_active = False
        self.current_wave_config = None

        self.camera_offset = None

        # Possible enemies for random waves
        self.possible_enemies = list(self.enemies_data.keys())

        #################### ANIMATION RELATED ATTRIBUTES ####################
        self.font = pygame.font.Font("fonts/pixel_font.ttf", 32)
        self.elapsed_time = 0
        self.animation_index = 0
        self.animation_active = False
        self.current_frame = None
        self.wave_display_start_time = 0
        #########################################################

        # Load wave counter frames
        self.beginning_frames = []
        self.progress_frames = []

        base_images_path = "images"
        wave_counter_path = os.path.join(base_images_path, "wave counter")
        beginning_folder_path = os.path.join(wave_counter_path, "beginning")

        # Load frames for beginning animation
        for file_name in sorted(os.listdir(beginning_folder_path)):
            frame_path = os.path.join(beginning_folder_path, file_name)
            frame = pygame.image.load(frame_path).convert_alpha()
            scaled_frame = pygame.transform.scale(frame, (250, 100))
            self.beginning_frames.append(scaled_frame)

        # Load progress frames
        for file_name in sorted(os.listdir(wave_counter_path)):
            frame_path = os.path.join(wave_counter_path, file_name)
            if os.path.isfile(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                scaled_frame = pygame.transform.scale(frame, (250, 100))
                self.progress_frames.append(scaled_frame)

        self.predefined_waves = [
            {"normal_fly": 3},  # Wave 1: 3 green_slimes
            {"green_slime": 5, "normal_fly": 2},  # Wave 2: 5 green_slimes, 2 normal_flies
            {"normal_fly": 5, "fire_fly": 3},  # Wave 3: 5 normal_flies, 3 fire_flies
            {"fire_fly": 4, "horse_ghost": 1},  # Wave 4: 4 fire_flies, 1 horse_ghost
            {"horse_ghost": 3, "electric_fly": 2},  # Wave 5: 3 horse_ghosts, 2 electric_flies
            {"electric_fly": 4, "myst_ghost": 1},  # Wave 6: 4 electric_flies, 1 myst_ghost
            {"myst_ghost": 2, "electric_enemy": 1},  # Wave 7: 2 myst_ghosts, 1 electric_enemy
            {"electric_enemy": 3, "myst_ghost": 2},  # Wave 8: 3 electric_enemies, 2 myst_ghosts
        ]

    def start_next_wave(self):
        self.is_wave_active = False
        self.current_wave += 1
        # resetting the enemies defeated counter at beginning of each wave
        self.enemies_defeated = 0

        # there are 8 predefined waves, if we are out of them, generate a random wave
        if self.current_wave <= len(self.predefined_waves):
            self.current_wave_config = self.predefined_waves[self.current_wave - 1]
        else:
            self.current_wave_config = self.generate_random_wave()

        self.total_enemies = sum(self.current_wave_config.values())  # Track total enemies

    def activate_wave(self, display):
        """Activates the wave animation."""
        if not self.is_wave_active:
            print(f"Activating wave {self.current_wave}!")
            self.is_wave_active = True
            self.animation_active = True
            self.animation_index = 0  # Reset animation frame index
            self.elapsed_time = 0  # Reset elapsed time
            self.wave_display_start_time = pygame.time.get_ticks()  # Track start time

    def update_wave_animation(self, display):
        """Updates the wave animation and handles fading out the text."""
        if self.animation_active:
            elapsed_time = pygame.time.get_ticks() - self.wave_display_start_time

            # Check if the animation should stop
            if elapsed_time > 5500:
                self.animation_active = False
                return
                # Prepare text properties
            wave_text = f"Wave {self.current_wave} Starting!"
            text_surface = self.font.render(wave_text, True, white)
            text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))

            # Calculate fade-out effect (255 -> 0 over 8 seconds)
            text_alpha = max(0, 255 - int((elapsed_time / 5500) * 255))
            text_surface.set_alpha(text_alpha)
            display.blit(text_surface, text_rect)

    def spawn_wave(self, wave_config, enemy_cooldown):
        # print(f"Spawning wave {self.current_wave} enemies...")
        for enemy_name, count in wave_config.items():
            for _ in range(count):
                enemy = Enemy(self.player, self.active_enemies, enemy_name, self.battle_area_rect)
                self.active_enemies.add(enemy)

    def display_counter(self, display):
        # Calculate progress based on enemies defeated
        if self.total_enemies > 0:
            progress_index = min(
                int((self.enemies_defeated / self.total_enemies) * (len(self.progress_frames) - 1)),
                len(self.progress_frames) - 1,
            )
            progress_frame = self.progress_frames[progress_index]

            # Display the progress frame
            display.blit(progress_frame, (195, 7))

    # todo: one of these must have a treasure chest
    def handle_enemy_drop(self, enemy):
        """Handles rewards dropped by a defeated enemy."""
        drop_chance = random.random()
        if drop_chance < 0.33:  # 33% chance to drop gold
            self.player.gold += 10
            print(f"Enemy {enemy.name} dropped gold! The player has {self.player.gold} gold")

    def update(self, display, frame_time, enemy_cooldown):
        """Updates the wave animation and ensures smooth transitions."""
        # display the announcement of the wave
        self.update_wave_animation(display)

        # entrance animation for the wave counter
        if self.animation_active:
            # Increment elapsed time
            self.elapsed_time += frame_time

            if self.elapsed_time >= 180:
                self.elapsed_time -= 180
                if self.animation_index < len(self.beginning_frames):
                    self.current_frame = self.beginning_frames[self.animation_index]
                    self.animation_index += 1
                else:
                    # turns off the animation parameter and in the next iteration the wave will start
                    self.animation_active = False
                    # spawning the enemies here so that they are spawned only once
                    self.spawn_wave(self.current_wave_config, enemy_cooldown)
                    self.player.is_fighting = True

            # while it isn't time to display the next frame, keep displaying the current one - avoid blinking
            if self.current_frame:
                display.blit(self.current_frame, (195, 7))

        else:
            # once the animations are over, start the actual wave
            self.camera_offset = calculate_camera_offset(self.player, display)
            self.display_counter(display)

            # updating and displaying the enemies
            self.active_enemies.update(frame_time)
            for enemy in self.active_enemies:
                display.blit(enemy.image, enemy.rect.topleft + self.camera_offset)

            # using a ratio instead of the whole rectangle because the transparent area of the images is too big
            collision_ratio = 0.5
            # adding the hit enemies to a group
            # Collision detection between two sprites, using rects scaled to a ratio:
            #                                           collide_rect_ratio(ratio) -> collided_callable
            collided_enemies = pygame.sprite.spritecollide(self.player.active_weapon, self.active_enemies, False,
                                                           collided=pygame.sprite.collide_rect_ratio(collision_ratio))
            # handling the loss of life of the enemies
            for enemy in collided_enemies:
                enemy.health -= self.player.active_weapon.damage
                print(f"Player hit {enemy.name}! Health: {enemy.health}")
                # info['score'] += 1
                if enemy.health <= 0:
                    enemy.kill()
                    self.handle_enemy_drop(enemy)
                    self.enemies_defeated += 1
                    print(f"Enemy {enemy.name} defeated! Total: {self.enemies_defeated}/{self.total_enemies}")

            # Collision detection between player and enemies
            collided_with_player = pygame.sprite.spritecollide(self.player, self.active_enemies, False,
                                                                collided=pygame.sprite.collide_rect_ratio(collision_ratio))

            for enemy in collided_with_player:
                current_time = pygame.time.get_ticks()
                if current_time - self.player.damage_cooldown > self.player.cooldown_duration:
                    self.player.health -= enemy.attack
                    # using this function to handle the display of the health bar (hearts) and game over,
                    # due to circular import
                    remove_health(enemy.attack)
                    print(f"Player hit by {enemy.name}! Health: {self.player.health}")
                    self.player.damage_cooldown = current_time

            if not self.active_enemies and self.is_wave_active:
                self.end_wave()

    def end_wave(self):
        print(f"Wave {self.current_wave} ended!")
        self.is_wave_active = False

        self.show_choice_popup()

    def show_choice_popup(self):
        message_lines = [f"Wave {self.current_wave} Completed!",
                         f"Start next wave or leave?"]

        # Starting position for the text
        start_x = 500
        start_y = 200
        line_spacing = 60

        button_image = pygame.image.load("images/store/store_button.png")
        next_wave_image = pygame.transform.scale(button_image, (250, 80))
        leave_image = pygame.transform.scale(button_image, (250, 80))
        next_wave_button = next_wave_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 75))
        leave_button = leave_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 160))

        # Wait for player input to make a choice
        choice_made = False
        while not choice_made:

            screen.blit(next_wave_image, next_wave_button.topleft)
            screen.blit(leave_image, leave_button.topleft)

            # Render buttons text
            next_wave_text = self.font.render("Next Wave", True, deep_black)
            leave_text = self.font.render("Leave", True, deep_black)

            for i, line in enumerate(message_lines):
                rendered_text = self.font.render(line, True, white)
                screen.blit(rendered_text, (start_x - i * 50, start_y + i * line_spacing))

            screen.blit(next_wave_text, (next_wave_button.centerx - next_wave_text.get_width() // 2,
                                         next_wave_button.centery - next_wave_text.get_height() // 2))
            screen.blit(leave_text, (leave_button.centerx - leave_text.get_width() // 2,
                                     leave_button.centery - leave_text.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_wave_button.collidepoint(event.pos):
                        self.start_next_wave()  # Start the next wave
                        choice_made = True
                    elif leave_button.collidepoint(event.pos):
                        self.is_wave_active = False  # End the wave
                        self.player.is_fighting = False  # Allow the player to leave the battle area rect
                        self.player.is_leaving_battle = True
                        choice_made = True

                pygame.display.update()