import random
import os
import pygame.time
from config import *
from enemy import Enemy
from utils import calculate_camera_offset
from weapon import Bow


class WaveManager:
    """
    Manages the enemy waves and related animations, spawn logic, and rewards in the game.

    Parameters
    ----------
    player : Player
        The player object interacting with the wave system.
    enemies_data : dict
        Data about the available enemies, including attributes like tier and health.
    battle_area_rect : pygame.Rect
        Defines the rectangular area where the battle takes place.

    Attributes
    ----------
    battle_area_rect : pygame.Rect
        The rectangular area where the battle occurs.
    player : Player
        The player object interacting with the wave system.
    current_wave : int
        The current wave number.
    is_wave_active : bool
        Indicates if the current wave is active.
    current_wave_config : dict
        Configuration for the current wave, including enemy types and counts.
    camera_offset : list or None
        Offset for camera adjustments in the battle area.
    enemies_data : dict
        Data about the available enemies.
    active_enemies : pygame.sprite.Group
        The group of enemies currently in the battle.
    enemies_defeated : int
        Count of enemies defeated in the current wave.
    total_enemies : int
        Total number of enemies in the current wave.
    possible_enemies : list
        The list of enemies available for random wave generation.
    enemy_cooldown : int
        Cooldown time in milliseconds between enemy spawns.
    last_enemy_spawn_time : int
        Timestamp of the last enemy spawn.
    enemies_to_spawn : list
        Queue of enemies waiting to spawn.
    font : pygame.font.Font
        The font used for displaying wave-related text.
    elapsed_time : int
        Time elapsed since the start of the wave animation.
    animation_index : int
        Index of the current animation frame.
    animation_active : bool
        Indicates if the wave animation is active.
    current_frame : pygame.Surface or None
        Current animation frame being displayed.
    wave_display_start_time : int
        Timestamp of when the wave display started.
    beginning_frames : list
        Frames for the beginning wave animation.
    progress_frames : list
        Frames for the progress wave animation (the animated counter of how much it is still left in the wave).
    predefined_waves : list
        The list of predefined wave configurations.

    """

    def __init__(self, player, enemies_data, battle_area_rect):

        self.battle_area_rect = battle_area_rect
        self.player = player
        self.current_wave = info['current_wave']
        self.is_wave_active = False
        self.current_wave_config = None
        self.camera_offset = None

        #################### ENEMY RELATED ATTRIBUTES ####################
        self.enemies_data = enemies_data
        self.active_enemies = pygame.sprite.Group()
        self.enemies_defeated = 0
        self.total_enemies = 0

        # Possible enemies for random waves
        self.possible_enemies = list(self.enemies_data.keys())

        self.enemy_cooldown = 2000  # Default cooldown in milliseconds
        self.last_enemy_spawn_time = 0
        self.enemies_to_spawn = []  # Queue for enemies waiting to spawn
        #####################################################################

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
            {"normal_fly": 10},  # Wave 1
            {"green_slime": 10, "normal_fly": 8},  # Wave 2
            {"normal_fly": 15, "fire_fly": 10},  # Wave 3
            {"fire_fly": 15, "horse_ghost": 10},  # Wave 4
            {"horse_ghost": 15, "electric_fly": 10},  # Wave 5
            {"electric_fly": 15, "myst_ghost": 10},  # Wave 6
            {"myst_ghost": 15, "electric_enemy": 10},  # Wave 7
            {"electric_enemy": 15, "myst_ghost": 10},  # Wave 8
        ]

    def start_next_wave(self):
        """
        Initializes the next wave, resetting counters and loading the appropriate configuration.
        If predefined waves are exhausted, a random wave is generated.
        """
        self.is_wave_active = False
        # resetting the enemies defeated counter at beginning of each wave
        self.enemies_defeated = 0

        # there are 8 predefined waves, if we are out of them, generate a random wave
        if info["current_wave"] <= len(self.predefined_waves):
            self.current_wave_config = self.predefined_waves[info["current_wave"] - 1]
        else:
            self.current_wave_config = self.generate_random_wave()

        self.total_enemies = sum(self.current_wave_config.values())  # Track total enemies

    def generate_random_wave(self):
        """
        Generates a random wave configuration based on the current wave.
        The number of enemies increases with the wave number, up to a maximum of 50.

        Returns
        -------
        dict
        A dictionary mapping enemy types to their counts for the wave.
        """
        # the more waves you do the bigger they become
        num_enemies = min(10 + info["current_wave"], 50)  # Stopping point: max 50 enemies

        # Generate a random wave configuration
        wave_config = {}
        for i in range(num_enemies):
            # considering tiers as weights for the random choice
            weights = [self.enemies_data[enemy]["tier"] for enemy in self.possible_enemies]
            chosen_enemy = random.choices(self.possible_enemies, weights=weights, k=1)[0]
            # takes the value of the key chosen enemy from the wave config dictionary and adds 1 to it
            wave_config[chosen_enemy] = wave_config.get(chosen_enemy, 0) + 1

        return wave_config

    def activate_wave(self):
        """
        Activates the wave by starting the animation and setting the wave state.
        Resets animation indices and prevents the player from leaving the battle area.
        """
        if not self.is_wave_active:
            self.is_wave_active = True
            self.animation_active = True
            self.animation_index = 0  # Reset animation frame index
            self.elapsed_time = 0  # Reset elapsed time
            self.wave_display_start_time = pygame.time.get_ticks()  # Track start time
            self.player.is_fighting = True  # Prevent the player from leaving the battle area rect

    def update_wave_animation(self, display):
        """
        Updates the wave animation, including fade-out effects and text rendering.

        Parameters
        ----------
        display : pygame.Surface
            The display surface where animations are rendered.
        """
        if self.animation_active:
            elapsed_time = pygame.time.get_ticks() - self.wave_display_start_time

            # Check if the animation should stop
            if elapsed_time > 5500:
                self.animation_active = False
                return
            # Prepare text properties
            wave_text = f"Wave {info['current_wave']} Starting!"
            text_surface = self.font.render(wave_text, True, white).convert_alpha()
            text_surface.set_colorkey((255, 255, 0))
            text_rect = text_surface.get_rect(center=(display.get_width() // 2, display.get_height() // 4))

            # Calculate fade-out effect (255 -> 0 over 8 seconds)
            text_alpha = max(0, 255 - int((elapsed_time / 5500) * 255))
            text_surface.set_alpha(text_alpha)

            display.blit(text_surface, text_rect)

    def spawn_wave(self, wave_config):
        """
        Adds enemies to the spawn queue based on the wave configuration.

        Parameters
        ----------
        wave_config : dict
            A dictionary mapping enemy types to their counts.
        """
        for enemy_name, count in wave_config.items():
            for _ in range(count):
                self.enemies_to_spawn.append(enemy_name)

    def display_counter(self, display):
        """
        Displays the wave progress counter on the screen.

        Parameters
        ----------
        display : pygame.Surface
            The display surface where the progress counter is rendered.
        """
        # Calculate progress based on enemies defeated
        if self.total_enemies > 0:
            progress_index = min(
                int((self.enemies_defeated / self.total_enemies) * (len(self.progress_frames) - 1)),
                len(self.progress_frames) - 1,
            )
            progress_frame = self.progress_frames[progress_index]

            # Display the progress frame
            display.blit(progress_frame, (195, 7))

    def handle_enemy_drop(self):
        """Handles the logic for enemy drops, giving rewards to the player with a 33% chance."""
        drop_chance = random.random()
        if drop_chance < 0.33:  # 33% chance to drop gold
            self.player.gold += 10

    def update(self, display, frame_time, power_up_manager):
        """
        Updates the game state, including animations, spawning, and player-enemy interactions.

        Parameters
        ----------
        display : pygame.Surface
            The display surface where game elements are rendered.
        frame_time : int
            The clock tick from the game.
        """
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

            # while it isn't time to display the next frame, keep displaying the current one - avoid blinking
            if self.current_frame:
                display.blit(self.current_frame, (195, 7))

        else:
            # once the animations are over, start the actual wave
            self.camera_offset = calculate_camera_offset(self.player, display)
            self.display_counter(display)
            if self.player.de_spawner:
                if len(self.active_enemies) > 2:
                    for enemy in self.active_enemies:
                        enemy.kill()
                        self.handle_enemy_drop()
                        self.enemies_defeated += 1

            # Enemy cooldown logic
            current_time = pygame.time.get_ticks()
            if self.enemies_to_spawn and current_time - self.last_enemy_spawn_time >= self.enemy_cooldown:
                enemy_name = self.enemies_to_spawn.pop(0)  # Get the next enemy to spawn
                enemy = Enemy(self.player, self.active_enemies, enemy_name, self.battle_area_rect)
                self.active_enemies.add(enemy)
                self.last_enemy_spawn_time = current_time  # Reset cooldown timer

            # updating and displaying the enemies
            self.active_enemies.update(frame_time)
            for enemy in self.active_enemies:
                display.blit(enemy.image, enemy.rect.topleft + self.camera_offset)

            # using a ratio instead of the whole rectangle because the transparent area of the images is too big
            collision_ratio = 0.5
            # adding the hit enemies to a group
            # Collision detection between two sprites, using rects scaled to a ratio:
            #                                           collide_rect_ratio(ratio) -> collided_callable
            if not isinstance(self.player.active_weapon, Bow):
                # Check collision directly with the weapon if it's not a Bow
                collided_enemies = pygame.sprite.spritecollide(self.player.active_weapon, self.active_enemies, False,
                                                               collided=pygame.sprite.collide_rect_ratio(
                                                                   collision_ratio))
            else:
                # Handle Bow specifically: Check collisions for each bullet in the Bow's group
                collided_enemies = []
                for bullet in self.player.active_weapon.bullets:
                    collided = pygame.sprite.spritecollide(bullet, self.active_enemies, False,
                                                           collided=pygame.sprite.collide_rect_ratio(collision_ratio))
                    # adding to the end of the list, not sure if it will cause problems otherwise
                    collided_enemies.extend(collided)

            for enemy in collided_enemies:
                current_time = pygame.time.get_ticks()
                if current_time - enemy.last_hit_time >= enemy.hit_cooldown:
                    enemy.last_hit_time = current_time
                    # the damage of the "bullets"/arrows of the bows is defined in the weapon damage attribute
                    enemy.health -= self.player.active_weapon.damage
                    if enemy.health <= 0:
                        enemy.kill()
                        self.handle_enemy_drop()
                        self.enemies_defeated += 1

            # Collision detection between player and enemies
            collided_with_player = pygame.sprite.spritecollide(self.player, self.active_enemies, False,
                                                               collided=pygame.sprite.collide_rect_ratio(
                                                                   collision_ratio))

            for enemy in collided_with_player:
                current_time = pygame.time.get_ticks()
                if current_time - self.player.damage_cooldown > self.player.cooldown_duration:
                    # this line updates the player's attribute
                    self.player.health -= enemy.attack
                    self.player.remove_health(enemy.attack)
                    if self.player.invincible:
                        enemy.kill()
                        self.handle_enemy_drop()
                        self.enemies_defeated += 1
                    self.player.damage_cooldown = current_time

            if self.total_enemies == self.enemies_defeated and self.is_wave_active and len(self.enemies_to_spawn) == 0:
                self.end_wave(power_up_manager)

    def end_wave(self, power_up_manager):
        """
        Ends the current wave, increments the wave counter, and shows a choice popup.
        """

        info["current_wave"] += 1
        self.current_wave = info["current_wave"]
        self.is_wave_active = False
        for power_up in power_up_manager.active_power_ups:
            power_up.deactivate(self.player)
        self.show_choice_popup()

    def show_choice_popup(self):
        """
        Displays a popup allowing the player to choose between starting the next wave or leaving.
        Handles rewards for completing the wave and updates the player state accordingly.
        """

        gold_reward = 50 * (info["current_wave"] - 1)
        self.player.add_gold(gold_reward)

        # putting 5 and 9 because at this point there was already an increment of the wave number
        bonus_reward = self.current_wave == 5 or self.current_wave == 9
        bonus_text = " and a bonus! Check your inventory." if bonus_reward else "!"

        message_lines = [f"Wave {info['current_wave'] - 1} Completed!",
                         f"You earned {gold_reward} gold{bonus_text}",
                         f"Start next wave or leave?"]

        if bonus_reward:
            self.player.give_bonus(self.current_wave)

        # Starting position for the text
        start_y = 200
        line_spacing = 60

        button_image = pygame.image.load("images/store/store_button.png").convert_alpha()
        button_image.set_colorkey((0, 0, 0))
        next_wave_image = pygame.transform.scale(button_image, (250, 80))
        leave_image = pygame.transform.scale(button_image, (300, 80))
        next_wave_button = next_wave_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 75))
        leave_button = leave_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 160))

        # Wait for player input to make a choice
        choice_made = False
        while not choice_made:
            screen.blit(next_wave_image, next_wave_button.topleft)
            screen.blit(leave_image, leave_button.topleft)

            # Render buttons text
            next_wave_text = self.font.render("Next Wave", True, deep_black, None).convert_alpha()
            leave_text = self.font.render("Save and Leave", True, deep_black, None).convert_alpha()

            for i, line in enumerate(message_lines):
                rendered_text = self.font.render(line, True, white, None).convert_alpha()
                # little thing so it appears on macbooks
                rendered_text.set_colorkey((255, 255, 0))
                text_width = rendered_text.get_width()
                x_position = (screen.get_width() - text_width) // 2  # Centered horizontally
                y_position = start_y + i * line_spacing  # Line spacing
                screen.blit(rendered_text, (x_position, y_position))

            screen.blit(next_wave_text, (next_wave_button.centerx - next_wave_text.get_width() // 2,
                                         next_wave_button.centery - next_wave_text.get_height() // 2))
            screen.blit(leave_text, (leave_button.centerx - leave_text.get_width() // 2,
                                     leave_button.centery - leave_text.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    progress()
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_wave_button.collidepoint(event.pos):
                        self.start_next_wave()  # Start the next wave
                        choice_made = True
                    elif leave_button.collidepoint(event.pos):
                        # adding 1 to the counter of the waves for the next time it enters the battle
                        # area the wave number will be already set
                        self.is_wave_active = False  # End the wave
                        self.player.is_fighting = False  # Allow the player to leave the battle area rect
                        self.player.is_leaving_battle = True
                        choice_made = True

                pygame.display.update()
