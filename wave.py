import random
import os
from config import *

from enemy import Enemy

class WaveManager:
    def __init__(self, player, enemies, battle_area_rect):

        self.font = pygame.font.Font("fonts/pixel_font.ttf", 32)
        self.current_wave = 0
        self.battle_area_rect = battle_area_rect
        self.enemies_data = enemies
        self.player = player
        self.active_enemies = pygame.sprite.Group()
        self.enemies_defeated = 0
        self.total_enemies = 0

        # Load wave counter frames
        self.beginning_frames = []
        self.progress_frames = []

        base_images_path = "images"
        wave_counter_path = os.path.join(base_images_path, "wave_counter")
        beginning_folder_path = os.path.join(wave_counter_path, "beginning")

        # Load frames for beginning animation
        for file_name in sorted(os.listdir(beginning_folder_path)):
            frame_path = os.path.join(beginning_folder_path, file_name)
            frame = pygame.image.load(frame_path).convert_alpha()
            self.beginning_frames.append(frame)

        # Load progress frames
        for file_name in sorted(os.listdir(wave_counter_path)):
            frame_path = os.path.join(wave_counter_path, file_name)
            if os.path.isfile(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                self.progress_frames.append(frame)

        self.predefined_waves = [
            {"green_slime": 3},  # Wave 1: 3 green_slimes
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

    def start_next_wave(self, display):
        self.current_wave += 1
        self.enemies_defeated = 0

        wave_text = f"Wave {self.current_wave} Starting!"
        text_surface = self.font.render(wave_text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))

        # Draw a "balloon" background
        balloon_rect = text_rect.inflate(20, 10)  # Add padding around the text
        pygame.draw.rect(display, (0, 0, 0), balloon_rect)  # Black rectangle as the balloon
        pygame.draw.rect(display, (255, 255, 255), balloon_rect, 3)  # White border

        # Blit text onto the screen
        display.blit(text_surface, text_rect)
        pygame.display.flip()

        # Pause briefly to show the wave announcement
        pygame.time.delay(2000)  # 2 seconds

        # Play beginning animation
        for frame in self.beginning_frames:
            display.blit(frame, frame.get_rect(center=(display.get_width() // 2, display.get_height() // 4)))
            pygame.display.flip()
            pygame.time.delay(300)  # Adjust delay as needed (300ms per frame)

        # there are 8 predefined waves, if we are out of them, generate a random wave
        if self.current_wave <= len(self.predefined_waves):
            wave_config = self.predefined_waves[self.current_wave - 1]
        else:
            wave_config = self.generate_random_wave()

        self.spawn_wave(wave_config)
        self.total_enemies = sum(wave_config.values())  # Track total enemies

    def spawn_wave(self, wave_config):
        for enemy_name, count in wave_config.items():
            for _ in range(count):
                # Spawn the enemy
                enemy = Enemy(self.player, self.active_enemies, enemy_name, self.battle_area_rect)
                self.active_enemies.add(enemy)
                self.active_enemies.update()

    def generate_random_wave(self):
        # the more waves you do the bigger they become
        num_enemies = min(10 + self.current_wave, 50)  # Stopping point: max 50 enemies

        # Generate a random wave configuration
        wave_config = {}
        for i in range(num_enemies):
            weights = [self.enemies_data[enemy]["tier"] for enemy in self.possible_enemies]
            chosen_enemy = random.choices(self.possible_enemies, weights=weights, k=1)[0]
            wave_config[chosen_enemy] = wave_config.get(chosen_enemy, 0) + 1

        return wave_config

    def reward_player(self, display):
        """Rewards the player and displays the reward message on the screen."""
        # Gold reward
        gold_reward = 50
        self.player.gold += gold_reward

        # Determine if a bonus reward is granted
        bonus_reward = random.random() < 0.3  # 30% chance
        bonus_text = " and a bonus!" if bonus_reward else "!"

        # Prepare reward message
        reward_text = f"Wave {self.current_wave} completed! You earned {gold_reward} gold{bonus_text}"
        text_surface = self.font.render(reward_text, True, (255, 255, 0))  # Yellow text
        text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))

        # Draw a "balloon" background
        balloon_rect = text_rect.inflate(20, 10)  # Add padding around the text
        pygame.draw.rect(display, (0, 0, 0), balloon_rect)  # Black rectangle as the balloon
        pygame.draw.rect(display, (255, 255, 255), balloon_rect, 3)  # White border

        # Blit text onto the screen
        display.blit(text_surface, text_rect)
        pygame.display.flip()

        pygame.time.delay(2000)

        # Apply bonus if granted
        if bonus_reward:
            self.player.give_bonus()  # todo: add this method to the player class

    def display_counter(self, display):
        # Calculate progress based on enemies defeated
        if self.total_enemies > 0:
            progress_index = min(
                int((self.enemies_defeated / self.total_enemies) * (len(self.progress_frames) - 1)),
                len(self.progress_frames) - 1,
            )
            progress_frame = self.progress_frames[progress_index]

            # Display the progress frame
            display.blit(progress_frame, (10, 10))  # Adjust position as needed

    def display_wave_completed_message(self, display):
        message = f"Wave {self.current_wave} completed!"
        text_color = white
        font_size = 48

        # Render the text
        font = pygame.font.Font("fonts/pixel_font.ttf", font_size)
        text_surface = font.render(message, True, text_color)
        text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 2))

        display.blit(text_surface, text_rect)
        pygame.display.flip()

        # Pause for a short duration
        pygame.time.delay(2000)  # Display the message for 2 seconds

    def update(self, display):
        # Check for defeated enemies
        for enemy in self.active_enemies:
            if enemy.health <= 0:
                self.active_enemies.remove(enemy)
                self.enemies_defeated += 1
                self.handle_enemy_drop(enemy)

        # Display progress frame
        self.display_counter(display)

        if not self.active_enemies:
            self.display_wave_completed_message(display)
            self.reward_player(display)
            self.start_next_wave(display)

# todo: one of these must have a treasure chest
    def handle_enemy_drop(self, enemy):
        """Handles rewards dropped by a defeated enemy."""
        drop_chance = random.random()
        if drop_chance < 0.2:  # 20% chance to drop gold
            print(f"Enemy {enemy.name} dropped gold!")
            self.player.gold += 10
        elif drop_chance < 0.3:  # Additional 10% chance to drop a health boost
            print(f"Enemy {enemy.name} dropped a health potion!")
            self.player.health += 5