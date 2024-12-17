import random
import os

import pygame.time

from config import *

from enemy import Enemy
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
        self.text_alpha = None
        self.text_rect = None
        self.text_surface = None
        self.wave_text = None
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
            {"normal_fly": 13},  # Wave 1: 3 green_slimes
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

            # Prepare text properties
            self.wave_text = f"Wave {self.current_wave} Starting!"
            self.text_surface = self.font.render(self.wave_text, True, white)
            self.text_rect = self.text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))
            self.text_alpha = 255  # Start fully opaque

    def update_wave_animation(self, display):
        """Updates the wave animation and handles fading out the text."""
        if self.animation_active:
            elapsed_time = pygame.time.get_ticks() - self.wave_display_start_time

            # Check if the animation should stop
            if elapsed_time > 5500:
                self.animation_active = False
                return

            # Calculate fade-out effect (255 -> 0 over 8 seconds)
            self.text_alpha = max(0, 255 - int((elapsed_time / 5500) * 255))
            self.text_surface.set_alpha(self.text_alpha)
            display.blit(self.text_surface, self.text_rect)

    def spawn_wave(self, wave_config):
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

    def update(self, display, frame_time):
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
                    self.spawn_wave(self.current_wave_config)
                    self.player.is_fighting = True

            # while it isn't time to display the next frame, keep displaying the current one - avoid blinking
            if self.current_frame:
                display.blit(self.current_frame, (195, 7))

        else:
            # once the animations are over, start the actual wave
            self.camera_offset = calculate_camera_offset(self.player, display)
            self.display_counter(display)

            """self.player.active_weapon_group.update(frame_time)
            for weapon in self.player.active_weapon_group:
                display.blit(weapon.image, weapon.rect.topleft + self.camera_offset)
                # print(weapon.image, weapon.rect.topleft)"""

            # updating and displaying the enemies
            self.active_enemies.update(frame_time)
            for enemy in self.active_enemies:
                display.blit(enemy.image, enemy.rect.topleft + self.camera_offset)

            # adding the hit enemies to a group
            collided_enemies = pygame.sprite.spritecollide(self.player.active_weapon, self.active_enemies, False)
            # handling the loss of life of the enemies
            for enemy in collided_enemies:
                enemy.health -= 5
                # info['score'] += 1
                if enemy.health <= 0:
                    enemy.kill()
                    self.enemies_defeated += 1
                    print(f"Enemy {enemy.name} defeated! Total: {self.enemies_defeated}/{self.total_enemies}")