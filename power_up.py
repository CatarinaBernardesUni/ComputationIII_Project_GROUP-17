from abc import ABC, abstractmethod
import pygame.transform
from player import Player
import random
from background import *

player = Player()


class PowerUp(ABC, pygame.sprite.Sprite):
    def __init__(self, pos, image, duration=5000):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.active = False
        self.start_time = None
        self.duration = duration

    def activate(self, player):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.affect_player(player)

    def update(self, player):
        """Deactivate power-up if duration has elapsed."""
        if self.active and pygame.time.get_ticks() - self.start_time > self.duration:
            self.deactivate(player)

    def deactivate(self, player):
        self.active = False
        # self.start_time = None  # Reset the timer
        player.remove_power_up()  # Remove the power-up from the player
        print("POWER UP REMOVED")

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
        pass

    def deactivate(self, player):
        super().deactivate(player)
        player.invincible = False


class Speed_Boost(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        player.speed += 2

    def affect_game(self, player):
        pass

    def deactivate(self, player):
        super().deactivate(player)
        player.speed -= 2


class De_Spawner(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        pass

    def affect_game(self, player):
        pass

    def deactivate(self, player):
        super().deactivate(player)
        pass


class Invisible(PowerUp):
    # enemies stop following the player
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

    def affect_player(self, player):
        player.invisible = True

    def affect_game(self, player):
        pass

    def deactivate(self, player):
        super().deactivate(player)
        player.invisible = False


class Chest(PowerUp):
    def __init__(self, pos, image):
        super().__init__(pos, image, duration=5000)

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

        # Starting positions and spacing for blitting images
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
                # pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 177 <= mouse[0] <= 429 and 247 <= mouse[1] <= 460:
                        chest = False
                    if 521 <= mouse[0] <= 770 and 247 <= mouse[1] <= 460:
                        chest = False
                    if 854 <= mouse[0] <= 1116 and 247 <= mouse[1] <= 460:
                        chest = False
            pygame.display.update()

    def affect_game(self, player):
        pass


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
                "probability": 0.05
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
        # classes = [ptype["class"] for ptype in self.power_up_types]
        probabilities = [ptype["probability"] for ptype in self.power_up_types]
        return random.choices(self.power_up_types, weights=probabilities, k=1)[0]

    def spawn_power_up(self):
        if not self.fight_area:
            raise ValueError("FIGHT AREA bounds not set! Use set_fight_area().")

        selected = self.choose_power_up()
        # Get a random position within the fight area
        x = random.randint(self.fight_area.left, self.fight_area.right)
        y = random.randint(self.fight_area.top, self.fight_area.bottom)

        print(f"Spawning power-up of type: {selected['class'].__name__} at ({x}, {y})")
        power_up = selected["class"]((x, y), selected["image"])
        self.active_power_ups.add(power_up)
        print(f"Total active power-ups: {len(self.active_power_ups)}")

    def update(self, player):
        """Periodically spawn power-ups and update active ones."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_power_up()
            self.last_spawn_time = current_time
        """        if not self.active_power_ups:
            if current_time - self.last_spawn_time > self.spawn_interval:
                self.spawn_power_up()
                self.last_spawn_time = current_time"""
        for power_up in list(self.active_power_ups):  # Use a copy of the list to avoid modifying it during iteration
            power_up.update(player)

        # Update active power-ups (check if any need deactivating)
        """for power_up in self.active_power_ups:
            power_up.update(player)"""

    def draw(self, screen, camera_offset):
        """Draw all active power-ups on the screen."""
        for power_up in self.active_power_ups:
            screen.blit(power_up.image, power_up.rect.topleft + camera_offset)
        # self.active_power_ups.draw(screen)

    def handle_collision(self, player):
        collided_power_ups = pygame.sprite.spritecollide(player, self.active_power_ups, dokill=True)
        for power_up in collided_power_ups:
            if not power_up.active:  # Activate the power-up only if it hasn't been activated
                print(f"Player picked up power-up: {type(power_up).__name__}")
                power_up.activate(player)  # Activate the power-up
        """for power_up in collided_power_ups:
            player.apply_power_up(power_up)
            print(f"Player collided with power-up: {type(power_up).__name__}")
            power_up.activate(player)  # Activate the power-up on collision
        Handle collisions between the player and active power-ups.

        collided_power_ups = pygame.sprite.spritecollide(player, self.active_power_ups, dokill=True)
        for power_up in collided_power_ups:
            print(f"Player collided with power-up: {type(power_up).__name__}")
            power_up.affect_player(player)"""

        # THE POWER UPS ARE BEING DRAWN IN THE INVENTORY SCREEN WHY???
