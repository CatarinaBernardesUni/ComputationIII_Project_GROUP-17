from abc import ABC, abstractmethod
import pygame.transform
from player import Player
import random
from background import *

player = Player()


def power_up_player_look(image, player):
    """
     Put an image on top of the player when they have the power up.

    Parameters
    ----------
    image: pygame.Surface
        The image to overlay on the player's frames.
    player: Player
        The player object whose appearance is being changed.

    """
    if not hasattr(player, "original_frames"):
        player.original_frames = {
            key: [frame.copy() for frame in frames]
            for key, frames in player.frames.items()
        }
    for key, frames in player.frames.items():
        for i in range(len(frames)):
            frame = frames[i].copy().convert_alpha()
            frame.blit(image, (7, 15))
            frames[i] = frame  # Update the frame with the overlay


class PowerUp(ABC, pygame.sprite.Sprite):
    """
    Initialize a PowerUp object.

        Parameters
        ----------
        pos: Tuple[int, int]
            The position where the power-up will be placed.
        image: pygame.Surface
            The image representing the power-up.
        duration: int, optional
            The duration for which the power-up is active (default is 10000 milliseconds).
    """

    def __init__(self, pos, image, duration=10000):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.active = False
        # tracks if power ups have been picked up
        self.collected = False
        self.start_time = None
        self.duration = duration

    def activate(self, player):
        """
        Activate the power-up, affecting the player and the game.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        self.active = True
        self.collected = True
        self.start_time = pygame.time.get_ticks()
        self.affect_player(player)
        self.affect_game(player)

    def update(self, player):
        """
        Deactivate power-up if duration has elapsed.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        if self.active and pygame.time.get_ticks() - self.start_time > self.duration:
            self.deactivate(player)

    def deactivate(self, player):
        """
        Deactivate the power-up and revert any changes made to the player.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        self.active = False
        self.collected = False
        self.start_time = None  # Reset the timer
        if hasattr(player, "original_frames"):
            player.frames = {
                key: [frame.copy() for frame in frames]
                for key, frames in player.original_frames.items()
            }
            del player.original_frames

    @abstractmethod
    def affect_game(self, player):
        """
         Abstract method to define how the power-up affects the game.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        pass

    @abstractmethod
    def affect_player(self, player):
        """
           Abstract method to define how the power-up affects the player.

        Parameters
        ----------
        player : Player
            The player who collected the power-up.

        """
        pass


class Invincibility(PowerUp):
    def affect_game(self, player):
        """
        Make the player invincible.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        player.invincible = True

    def affect_player(self, player):
        """
        Change the player's appearance to indicate invincibility.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.
        """
        power_up_player_look(power_up_invincibility, player)

    def deactivate(self, player):
        """
        Deactivate the invincibility power-up and revert the player's invincibility.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        super().deactivate(player)
        player.invincible = False


class SpeedBoost(PowerUp):
    def affect_game(self, player):
        """
       Increase the player's speed.

       Parameters
       ----------
       player: Player
           The player who collected the power-up.

       """
        player.speed += 2

    def affect_player(self, player):
        """
        Change the player's appearance to indicate a speed boost.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        power_up_player_look(power_up_speed, player)

    def deactivate(self, player):
        """
        Deactivate the speed boost power-up and revert the player's speed.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        super().deactivate(player)  # Reset the active state
        player.speed -= 2


class DeSpawner(PowerUp):
    def affect_game(self, player):
        """
        Prevent enemies from spawning.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        player.de_spawner = True

    def affect_player(self, player):
        """
        Change the player's appearance to indicate the de-spawner effect.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        power_up_player_look(power_up_de_spawner, player)

    def deactivate(self, player):
        """
        Deactivate the de-spawner power-up and allow enemies to spawn again.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        super().deactivate(player)  # Reset the active state
        player.de_spawner = False

class Invisible(PowerUp):
    # enemies stop following the player
    def affect_game(self, player):
        """
        Make the player invisible to enemies.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        player.invisible = True

    def affect_player(self, player):
        """
        Change the player's appearance to indicate invisibility.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        power_up_player_look(power_up_invisible, player)

    def deactivate(self, player):
        """
        Deactivate the invisibility power-up and make the player visible to enemies again.

        Parameters
        ----------
        player: Player
            The player who collected the power-up.

        """
        super().deactivate(player)  # Reset the active state
        player.invisible = False


class Chest(PowerUp):
    """
    Initialize a Chest object.

        Parameters
        ----------
        pos: Tuple[int, int]
            The position where the chest will be placed.
        image: pygame.Surface
            The image representing the chest.

    """

    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.current_power_up = None

    def affect_game(self, player):
        """
        Display the chest and allow the player to choose a power-up.

        Parameters
        ----------
        player: Player
            The player who collected the chest.

        """
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

        x_start = (width - 1000) // 2 + 50
        y_start = (height - 300) // 2 + 35
        spacing = 340

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

    def affect_player(self, player):
        """
        This method is intentionally left blank as the chest itself does not affect the player directly.

        Parameters
        ------------
        player: Player

        """
        pass

    def deactivate(self, player):
        """
        Deactivate the chest and any power-up it granted.

        Parameters
        ----------
        player: Player
            The player who collected the chest.

        """
        super().deactivate(player)
        if self.current_power_up and self.current_power_up.active:
            self.current_power_up.deactivate(player)
            self.current_power_up = None  # Reset the tracked power-up


class PowerUpManager:
    """
    Manages the spawning, updating, and handling of power-ups in the game.

    Parameters
    ----------
    map_width: int
        The width of the map.
    map_height: int
        The height of the map.
    spawn_interval: int, optional
        The interval in milliseconds between power-up spawns, by default 30000 (30 seconds).

    Notes
    ------
    The PowerUpManager is responsible for:
    - Spawning power-ups at random intervals within a specified fight area.
    - Managing the active power-ups, including their positions and states.
    - Handling collisions between the player and power-ups, activating their effects.
    - Drawing the power-ups on the screen with appropriate camera offsets.

    """

    def __init__(self, map_width, map_height, spawn_interval=30000):  # 30 seconds until next power up
        self.map_width = map_width
        self.map_height = map_height
        self.spawn_interval = spawn_interval
        self.last_spawn_time = pygame.time.get_ticks()
        self.active_power_ups = pygame.sprite.Group()
        self.fight_area = None

        # POWER UPS
        self.power_up_types = [
            {
                "class": Invincibility,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up1.png"), (50, 50)),
                "probability": 0.1
            },
            {
                "class": SpeedBoost,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up2.png"), (50, 50)),
                "probability": 0.2
            },
            {
                "class": Chest,
                "image": pygame.transform.scale(pygame.image.load("images/chests/chest_brown.png"), (50, 50)),
                "probability": 0.05
            },
            {
                "class": DeSpawner,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up3.png"), (50, 50)),
                "probability": 0.35
            },
            {
                "class": Invisible,
                "image": pygame.transform.scale(pygame.image.load("images/others/power_up4.png"), (50, 50)),
                "probability": 0.3
            }
        ]

    def set_fight_area(self, fight_area):
        """
        Set the bounds for the fight area where power-ups should spawn.

        Parameters
        ----------
        fight_area: pygame.Rect
            The rectangular area within which power-ups can spawn.
        """
        if isinstance(fight_area, pygame.Rect):
            self.fight_area = fight_area

    def choose_power_up(self):
        """
        Choose a power-up class based on defined probabilities.

        Returns
        -------
        dict
            A dictionary containing the selected power-up class, image, and probability.

        """
        probabilities = [ptype["probability"] for ptype in self.power_up_types]
        return random.choices(self.power_up_types, weights=probabilities, k=1)[0]

    def spawn_power_up(self):
        """
        Spawn a power-up at a random position within the fight area.

        """
        selected = self.choose_power_up()
        # Get a random position within the fight area
        x = random.randint(self.fight_area.left, self.fight_area.right)
        y = random.randint(self.fight_area.top, self.fight_area.bottom)

        power_up = selected["class"]((x, y), selected["image"])
        self.active_power_ups.add(power_up)

    def update(self, player):
        """
        Update the state of the power-ups and spawn new ones periodically.

        Parameters
        ----------
        player: Player
            The player object to check for power-up interactions.

        """

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
            if player not in self.fight_area:
                self.active_power_ups.remove(power_up)

    def draw(self, screen, camera_offset):
        """
        Draw the active power-ups on the screen with the appropriate camera offset.

        Parameters
        ----------
        screen: pygame.Surface
            The surface to draw the power-ups on.
        camera_offset: Tuple[int, int]
            The offset to apply to the power-up positions for camera movement.
        """
        for power_up in self.active_power_ups:
            screen.blit(power_up.image.convert_alpha(), power_up.rect.topleft + camera_offset)
            # this camera offset is used so that the power ups stay in place and don't move with the player moving

    def handle_collision(self, player):
        """
        Handle collisions between the player and power-ups, activating their effects.

        Parameters
        ----------
        player : Player
            The player object to check for collisions with power-ups.

        """
        collided_power_ups = pygame.sprite.spritecollide(player, self.active_power_ups, dokill=False)
        for power_up in collided_power_ups:
            if not power_up.collected:  # Pick up the power-up only if not already collected
                power_up.activate(player)  # Activate the power-ups effects
                power_up.collected = True  # Mark it as collected
