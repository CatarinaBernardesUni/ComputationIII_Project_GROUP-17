from abc import ABC, abstractmethod
import pygame.transform
from player import Player
import random
from background import *

player = Player()


def power_up_player_look(image, player):
    if not hasattr(player, "original_frames"):
        player.original_frames = {
            key: [frame.copy() for frame in frames]
            for key, frames in player.frames.items()
        }
    for key, frames in player.frames.items():
        for i in range(len(frames)):
            frame = frames[i].copy()  # Copy the original frame
            frame.blit(image, (7, 15))  # Blit the overlay on the frame
            frames[i] = frame  # Update the frame with the overlay


class PowerUp(ABC, pygame.sprite.Sprite):
    def __init__(self, pos, image, duration=5000):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.active = False
        # tracks if power ups have been picked up
        self.collected = False
        self.start_time = None
        self.duration = duration

    def activate(self, player):
        self.active = True
        self.collected = True
        self.start_time = pygame.time.get_ticks()
        self.affect_player(player)
        self.affect_game(player)

    def update(self, player):
        """Deactivate power-up if duration has elapsed."""
        if self.active and pygame.time.get_ticks() - self.start_time > self.duration:
            self.deactivate(player)

    def deactivate(self, player):
        self.active = False
        self.collected = False
        self.start_time = None  # Reset the timer
        print(f"Deactivated and removed: {type(self).__name__}")
        if hasattr(player, "original_frames"):
            player.frames = {
                key: [frame.copy() for frame in frames]
                for key, frames in player.original_frames.items()
            }
            del player.original_frames

    # abstract methods need to be implemented in the other child classes the power ups
    @abstractmethod
    def affect_player(self, player):
        pass

    @abstractmethod
    def affect_game(self, player):
        pass


class Invincibility(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        player.invincible = True

    def affect_game(self, player):
        power_up_player_look(power_up_invincibility, player)

    def deactivate(self, player):
        super().deactivate(player)  # Reset the active state
        player.invisible = False
        print("Player is no longer invisible.")


class Speed_Boost(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        player.speed += 2

    def affect_game(self, player):
        power_up_player_look(power_up_speed, player)

    def deactivate(self, player):
        super().deactivate(player)  # Reset the active state

        player.speed -= 2
        print("Player is no longer fast.")


class De_Spawner(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        pass

    def affect_game(self, player):
        power_up_player_look(power_up_de_spawner, player)

    def deactivate(self, player):
        super().deactivate(player)  # Reset the active state
        print("Enemies will now spawn.")


class Invisible(PowerUp):
    # enemies stop following the player
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        player.invisible = True

    def affect_game(self, player):
        power_up_player_look(power_up_invisible, player)

    def deactivate(self, player):
        super().deactivate(player)  # Reset the active state
        player.invisible = False
        print("Player is no longer invisible.")


class Chest(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)
        self.current_power_up = None

    def affect_player(self, player):
        chest = True
        screen.blit(chest_choice, ((width - 1000) // 2, (height - 300) // 2))
        screen.blit(pick_powerup, (width // 2 - 200, 10))

        # CHEST CHOICES HERE
        powerup_manager = PowerUpManager(width, height)
        filtered_power_ups = []
        for power_up in powerup_manager.power_up_types:
            if power_up["class"] != Chest:
                filtered_power_ups.append(power_up)

        # Select 3 unique random power-ups
        choices = random.sample(filtered_power_ups, 3)

        x_start = (width - 1000) // 2 + 50  # Starting x-coordinate
        y_start = (height - 300) // 2 + 30  # Starting y-coordinate
        spacing = 340  # Space between the images

        # Loop through the selected choices and blit their images to the screen
        for i, choice in enumerate(choices):
            image = pygame.transform.scale(choice["image"], (200, 200))  # Access the image from the power-up dictionary
            x_pos = x_start + i * spacing  # Calculate x position
            screen.blit(image, (x_pos, y_start))

        while chest:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    progress()
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the player selects one of the three power-ups
                    selected_power_up = None
                    if 177 <= mouse[0] <= 429 and 247 <= mouse[1] <= 460:
                        selected_power_up = choices[0]
                    elif 521 <= mouse[0] <= 770 and 247 <= mouse[1] <= 460:
                        selected_power_up = choices[1]
                    elif 854 <= mouse[0] <= 1116 and 247 <= mouse[1] <= 460:
                        selected_power_up = choices[2]

                    if selected_power_up:
                        self.current_power_up = selected_power_up["class"]((0, 0), selected_power_up["image"])
                        self.current_power_up.activate(player)
                        chest = False

            pygame.display.update()

    def affect_game(self, player):
        pass

    def deactivate(self, player):
        super().deactivate(player)
        if self.current_power_up and self.current_power_up.active:
            self.current_power_up.deactivate(player)
            print(f"Deactivated power-up from Chest: {type(self.current_power_up).__name__}")
            self.current_power_up = None  # Reset the tracked power-up


class PowerUpManager:
    def __init__(self, map_width, map_height, spawn_interval=10000,
                 duration=5000):  # 30 seconds until next power up (the 1st one
        # also takes 30 seconds to appear)
        self.map_width = map_width
        self.map_height = map_height
        self.spawn_interval = spawn_interval
        self.duration = duration
        self.last_spawn_time = pygame.time.get_ticks()
        self.active_power_ups = pygame.sprite.Group()
        self.fight_area = None

        # POWER UPS
        self.power_up_types = [
            {
                "class": Invincibility,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up1.png"), (50, 50)),
                "probability": 0.05
            },
            {
                "class": Speed_Boost,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up2.png"), (50, 50)),
                "probability": 0.8
            },
            {
                "class": Chest,
                "image": pygame.transform.scale(pygame.image.load("images/chests/chest_brown.png"), (50, 50)),
                "probability": 0.8
            },
            {
                "class": De_Spawner,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up3.png"), (50, 50)),
                "probability": 0.05
            },
            {
                "class": Invisible,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up4.png"), (50, 50)),
                "probability": 0.05
            }
        ]

    def set_fight_area(self, fight_area):
        """Set the bounds for the fight area where power-ups should spawn."""
        if isinstance(fight_area, pygame.Rect):
            self.fight_area = fight_area

    def choose_power_up(self):
        """Choose a power-up class based on defined probabilities."""
        probabilities = [ptype["probability"] for ptype in self.power_up_types]
        return random.choices(self.power_up_types, weights=probabilities, k=1)[0]

    def spawn_power_up(self):
        selected = self.choose_power_up()
        # Get a random position within the fight area
        x = random.randint(self.fight_area.left, self.fight_area.right)
        y = random.randint(self.fight_area.top, self.fight_area.bottom)

        print(f"Spawning power-up of type: {selected['class'].__name__} at ({x}, {y})")
        power_up = selected["class"]((x, y), selected["image"])
        self.active_power_ups.add(power_up)
        print(f"Total active power-ups: {len(self.active_power_ups)}")

    def update(self, player):

        current_time = pygame.time.get_ticks()

        # Spawn new power-ups periodically
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_power_up()
            self.last_spawn_time = current_time

        # Check each power-up for updates
        for power_up in list(self.active_power_ups):  # Use a copy to safely modify the group
            if power_up.collected:  # Only update if the power-up has been picked up
                power_up.update(player)

                # Remove if the power-up has expired
                if not power_up.active:  # Duration expired
                    self.active_power_ups.remove(power_up)
                    print(f"Deactivated and removed power-up: {type(power_up).__name__}")

        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_power_up()
            self.last_spawn_time = current_time
        for power_up in list(self.active_power_ups):  # Use a copy of the list to avoid modifying it during iteration
            power_up.update(player)
            if not power_up.active:
                self.active_power_ups.remove(power_up)
                print(f"Removed power-up: {type(power_up).__name__}")"""

    def draw(self, screen, camera_offset):
        for power_up in self.active_power_ups:
            screen.blit(power_up.image, power_up.rect.topleft + camera_offset)
            # this camera offset is used so that the power ups stay in place and don't move with the player moving

    def handle_collision(self, player):
        """collided_power_ups = pygame.sprite.spritecollide(player, self.active_power_ups, dokill=False)
        for power_up in collided_power_ups:
            if not power_up.collected:  # Only activate if not already picked up
                print(f"Player picked up power-up: {type(power_up).__name__}")
                power_up.activate(player)  # Activate the power-up's effects
                power_up.collected = True  # Mark it as collected

                # Remove the sprite visually
                self.active_power_ups.remove(power_up)"""
        # this code ^^ makes the image disappear after, but not its effects
        # in chest the effects just don't disappear

        collided_power_ups = pygame.sprite.spritecollide(player, self.active_power_ups, dokill=False)
        for power_up in collided_power_ups:
            if not power_up.collected:  # Pick up the power-up only if not already collected
                print(f"Player picked up power-up: {type(power_up).__name__}")
                power_up.activate(player)  # Activate the power-ups effects
                power_up.collected = True  # Mark it as collected
        # this code makes the deactivation work but the power up image stays in the game until its effect is gone
