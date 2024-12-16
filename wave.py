import random
import os

import pygame.time

from config import *

from enemy import Enemy
from utils import calculate_camera_offset


# todo: everything color related should be in config.py
# todo: added too many display.flip(), how frequently should this be called?
class WaveManager:
    def __init__(self, player, enemies_data, battle_area_rect):

        self.text_alpha = None
        self.text_rect = None
        self.text_surface = None
        self.wave_text = None
        self.wave_display_start_time = None
        self.font = pygame.font.Font("fonts/pixel_font.ttf", 32)
        self.battle_area_rect = battle_area_rect
        self.enemies_data = enemies_data
        self.player = player
        self.active_enemies = pygame.sprite.Group()
        self.current_wave = 0
        self.enemies_defeated = 0
        self.total_enemies = 0
        self.is_wave_active = False
        self.current_wave_config = None
        self.animation_countdown = 0

        self.camera_offset = None

        #################### HELL ATTRIBUTES ####################
        self.wave_timer = 0  # Initialize wave timer

        self.animation_index = 0
        self.animation_timer = 0  # Track time for frame updates

        self.animation_active = False
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

        # Possible enemies for random waves
        self.possible_enemies = list(self.enemies_data.keys())

    def start_next_wave(self):
        self.is_wave_active = False
        self.current_wave += 1
        self.enemies_defeated = 0

        # there are 8 predefined waves, if we are out of them, generate a random wave
        if self.current_wave <= len(self.predefined_waves):
            self.current_wave_config = self.predefined_waves[self.current_wave - 1]
        else:
            self.current_wave_config = self.generate_random_wave()

        self.total_enemies = sum(self.current_wave_config.values())  # Track total enemies

    """def activate_wave(self, display, event_display_start_wave_message):
        #Activates the wave and displays the wave announcement.
        if not self.is_wave_active:
            print(f"Activating wave {self.current_wave}!")
            self.is_wave_active = True
            self.animation_index = 0
            self.animation_active = True
            self.animation_timer = pygame.time.get_ticks()

            pygame.time.set_timer(event_display_start_wave_message, 10000)

            wave_text = f"Wave {self.current_wave} Starting!"
            text_surface = self.font.render(wave_text, True, white)  # White text
            text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))

            # Draw a "balloon" background
            balloon_rect = text_rect.inflate(20, 10)  # Add padding around the text
            pygame.draw.rect(display, deep_black, balloon_rect)  # Black rectangle as the balloon
            pygame.draw.rect(display, white, balloon_rect, 3)  # White border

            # Blit text onto the screen
            display.blit(text_surface, text_rect)"""

    def activate_wave(self, display):
        """Activates the wave animation using frame time."""
        if not self.is_wave_active:
            print(f"Activating wave {self.current_wave}!")
            self.is_wave_active = True
            self.animation_active = True
            self.wave_display_start_time = pygame.time.get_ticks()  # Log the start time

            # Prepare text and its properties
            self.wave_text = f"Wave {self.current_wave} Starting!"
            self.text_surface = self.font.render(self.wave_text, True, white)
            self.text_rect = self.text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))
            self.text_alpha = 255  # Start fully opaque

    def update_wave_animation(self, display, frame_time):
        """Updates the wave animation and handles fading out the text."""
        if self.animation_active:
            elapsed_time = pygame.time.get_ticks() - self.wave_display_start_time

            # Check if the animation should stop (5 seconds total)
            if elapsed_time > 5000:
                self.animation_active = False  # Stop the animation
                return

            # Calculate fade-out effect (255 -> 0 over 5 seconds)
            self.text_alpha = max(0, 255 - int((elapsed_time / 5000) * 255))
            # self.text_surface.set_alpha(self.text_alpha)

            # Draw the text with fade effect
            balloon_rect = self.text_rect.inflate(20, 10)  # Add padding around the text

            # Blit the text onto the display
            display.blit(self.text_surface, self.text_rect)

    def spawn_wave(self, wave_config):
        print(f"Spawning wave {self.current_wave} enemies...")
        for enemy_name, count in wave_config.items():
            for _ in range(count):
                enemy = Enemy(self.player, self.active_enemies, enemy_name, self.battle_area_rect)
                print(f"Spawned {enemy_name}!")
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
            display.blit(progress_frame, (195, 7))  # Adjust position as needed

    def update(self, display, frame_time):
        if self.animation_active:
            self.animation_timer += frame_time
            # Handle beginning frames animation
            if self.animation_timer >= 240:
                self.animation_timer -= 240
                if self.animation_index < len(self.beginning_frames):
                    frame = self.beginning_frames[self.animation_index]
                    display.blit(frame, (195, 7))
                    self.animation_index += 1
                else:
                    self.animation_active = False
                    print("Animation completed.")
                    # self.start_next_wave()
                    self.spawn_wave(self.current_wave_config)

        if not self.animation_active:
            self.camera_offset = calculate_camera_offset(self.player, display)
            # Display progress bar after animation finishes
            self.display_counter(display)

            for enemy in self.active_enemies:
                #print(f"Rendering enemy at {enemy.rect.topleft + self.camera_offset}")
                display.blit(enemy.image, enemy.rect.topleft + self.camera_offset)