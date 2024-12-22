import pygame
from os.path import join
from os import walk  # allows us to walk through a folder
import config
from dog import Dog
from weapon import *


# making a player a child of the Sprite class
class Player(pygame.sprite.Sprite):  # sprites are moving things in pygame
    """
    A class that represents the player in the game.

    Attributes
    ----------
    font : pygame.font.Font
        The font used for rendering text associated with the player.
    user : str
        The selected character for the player.
    state : str
        The current state of the player's animation (e.g., "left", "idle").
    frame_index : int
        The index of the current animation frame.
    image : pygame.Surface
        The current visual representation of the player sprite.
    rect : pygame.Rect
        The rectangle defining the position and dimensions of the player for rendering and collisions.
    hitbox_rect : pygame.Rect
        A smaller rectangle for precise collision detection.
    dog : Dog
        The player's dog companion, if purchased.
    just_left_cave : bool
        Indicates whether the player has just left the cave.
    just_left_old_lady_house : bool
        Indicates whether the player has just left the old lady's house.
    just_left_home : bool
        Indicates whether the player has just left their home.
    just_left_store : bool
        Indicates whether the player has just left the store.
    just_left_pink_house : bool
        Indicates whether the player has just left the pink house.
    just_left_shed : bool
        Indicates whether the player has just left the shed.
    just_left_greenhouse : bool
        Indicates whether the player has just left the greenhouse.
    is_fighting : bool
        Indicates whether the player is currently in a battle.
    is_leaving_battle : bool
        Indicates whether the player is leaving a battle area.
    speed : int
        The player's movement speed.
    health : int
        The player's current health.
    max_health : int
        The player's maximum health.
    bullet_cooldown : int
        The cooldown time (in frames) for firing bullets.
    damage_cooldown : int
        The cooldown time (in milliseconds) for taking damage.
    cooldown_duration : int
        The duration (in milliseconds) of the damage cooldown.
    invincible : bool
        Indicates whether the player is invincible.
    active_power_ups : list
        A list of active power-ups affecting the player.
    invisible : bool
        Indicates whether the player is invisible to enemies.
    de_spawner : bool
        Indicates whether the player has the ability to prevent enemies from spawning.
    inventory : dict
        A dictionary representing the player's inventory items and their quantities.
    gold : int
        The amount of gold the player currently has.
    price_items : dict
        A dictionary mapping item names to their prices in gold.
    health_boosts : dict
        A dictionary mapping item names to the amount of health they restore.
    active_weapon : pygame.sprite.Sprite or None
        The currently active weapon equipped by the player.
    active_weapon_group : pygame.sprite.Group
        A sprite group containing the player's active weapon.
    """

    def __init__(self):
        # calling the mother classes init aka Sprite
        super().__init__()
        self.font = pygame.font.Font("fonts/pixel_font.ttf", 16)
        self.user = config.character_choice
        self.load_images()  # we need to do this before creating image
        self.state, self.frame_index = "left", 0
        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)  # we use surface to display any image or draw
        # area where the player will be drawn
        self.rect = self.image.get_rect()
        # initial position of the player
        self.rect.center = (1150, 150)
        # making the hitbox smaller than the player image
        self.hitbox_rect = self.rect.inflate(-10, -15)

        # being able to receive a dog:
        self.dog = Dog(self)

        # GAMEPLAY VARIABLES
        self.just_left_cave = False
        self.just_left_old_lady_house = False
        self.just_left_home = False
        self.just_left_store = False
        self.just_left_pink_house = False
        self.just_left_shed = False
        self.just_left_greenhouse = False

        self.is_fighting = False
        self.is_leaving_battle = False
        self.speed = 3
        self.health = info['health']
        self.max_health = 10
        # to be able to get more hearts in the game
        self.bullet_cooldown = 0
        self.damage_cooldown = 0  # Initial cooldown time
        self.cooldown_duration = 2000

        # POWER-UPS
        self.invincible = False
        self.active_power_ups = []
        self.invisible = False
        self.de_spawner = False

        # INVENTORY AND MONEY (GOLD) START WITH 200
        self.inventory = info['inventory']
        self.gold = info['gold']

        # storing the inventory prices
        self.price_items = {'apple': 30,
                            'mushroom': 50,
                            'speed potion': 70,
                            'dog': 200,
                            'soup': 100,
                            'dagger': 100,
                            'ghost_bow': 200,
                            'key': 300}
        self.health_boosts = {"apple": 1, "mushroom": 2, "soup": 5}

        ########### WEAPONS ########################
        self.active_weapon = None  # Currently active weapon
        self.active_weapon_group = pygame.sprite.Group()  # Group to store the active weapon

    ############################## METHODS TO DEAL WITH WEAPONS ########################################
    def switch_weapon(self, weapon_name, weapon_type):
        """
        Function to be able to switch the currently active weapon.

        Parameters
        ----------
        weapon_name: str
            the name of the weapon the user wants to switch to
        weapon_type: str
            the type of the weapon (e.g. "Sword", "Bow", "Axe")

        """
        if self.active_weapon_group is not None:
            self.active_weapon_group.remove(self.active_weapon)
        if weapon_type == "Sword":
            weapon_instance = Sword(self, self.active_weapon_group, weapon_name)
        elif weapon_type == "Bow":
            weapon_instance = Bow(self, self.active_weapon_group, weapon_name)
        else:  # a weapon will always be one of these 3 types
            weapon_instance = Axe(self, self.active_weapon_group, weapon_name)
        self.active_weapon = weapon_instance
        self.active_weapon_group.add(self.active_weapon)

    ###### CRYSTALS ####################################################################################
    def collect_crystal(self, crystal_name):
        """
        Add a crystal instance to the player's inventory.

        Parameters
        ----------
        crystal_name : str
            The name of the crystal to collect.
        """
        info['inventory'][crystal_name] += 1
        self.inventory = info['inventory']

    ############### ANIMATION AND MOVEMENT ############################################################

    def load_images(self):
        """
        The images for the player character and store them in the frames dictionary.

        """
        self.frames = {"up": [], "down": [], "left": [], "right": [],
                       "idle_down": [], "idle_up": [], "idle_left": [], "idle_right": []}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("images", "player", self.user, state)):
                if file_names:
                    for file_name in file_names:
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        scaled_surf = pygame.transform.scale(surf, player_size)
                        self.frames[state].append(scaled_surf)

    def animate(self):
        """
        Update the player's animation by the frame index and setting the current image.

        """
        self.frame_index += 0.08  # increments frame index at a fixed fps (animation speed)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def draw_hearts(self, display):
        """
        Draw the player's health hearts on the display.

        Parameters
        ----------
        display: pygame.Surface
            The surface on which to draw the hearts.

        """
        for heart in range(self.max_health):
            if heart < info['health']:
                display.blit(full_heart, (heart * 33, 5))
            else:
                display.blit(empty_heart, (heart * 33, 5))

    def update(self, collision_sprites, display, frame_time, battle_area_rect=None):
        """
        Update the player's state, handle movement, animation, and drawing.

        Parameters
        ----------
        collision_sprites: pygame.sprite.Group
            The group of sprites to check for collisions.
        display: pygame.Surface
            The surface on which to draw the player and other elements.
        frame_time: float
            The time elapsed since the last frame.
        battle_area_rect: pygame.Rect, optional
            The rectangular area defining the battle zone.

        """


        keys = pygame.key.get_pressed()
        movement = False
        # checking which keys where pressed and moving the player accordingly
        # independent movements, independent ifs

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.rect.y -= self.speed
            self.state = "up"
            movement = True
            self.hitbox_rect.centery = self.rect.centery
            self.collision('vertical', collision_sprites)
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            self.rect.y += self.speed
            self.state = "down"
            movement = True
            self.hitbox_rect.centery = self.rect.centery
            self.collision('vertical', collision_sprites)
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.x -= self.speed
            self.state = "left"
            movement = True
            self.hitbox_rect.centerx = self.rect.centerx
            self.collision('horizontal', collision_sprites)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < width:
            self.rect.x += self.speed
            self.state = "right"
            movement = True
            self.hitbox_rect.centerx = self.rect.centerx
            self.collision('horizontal', collision_sprites)

        if not movement:
            if self.state == "down":
                self.state = "idle_down"
            elif self.state == "up":
                self.state = "idle_up"
            elif self.state == "left":
                self.state = "idle_left"
            elif self.state == "right":
                self.state = "idle_right"
        self.animate()
        self.draw_hearts(display)
        self.dont_leave_battle(battle_area_rect)

        if self.active_weapon is None and battle_area_rect is not None:
            if battle_area_rect.colliderect(self.rect):
                message_lines = [
                    "You better find a weapon before you start fighting,",
                    "explore a bit more....",
                    "I heard that there is a store somewhere in here...",
                    "to activate a weapon go to your inventory and click on it"]

                # Starting position for the text
                start_x = 100
                start_y = 70
                line_spacing = 30  # Spacing between lines
                # Render each line and blit to the screen
                for i, line in enumerate(message_lines):
                    rendered_text = self.font.render(line, True, white)
                    display.blit(rendered_text, (start_x, start_y + i * line_spacing))

                if self.rect.right > battle_area_rect.left:
                    self.rect.right = battle_area_rect.left

    def dont_leave_battle(self, battle_area_rect):
        """
        While in battle the player is not able to leave the battle area.

        Parameters
        ----------
        battle_area_rect : pygame.Rect
            The rectangular area defining the battle zone.

        """
        if self.is_fighting:
            if self.rect.left < battle_area_rect.left:
                self.rect.left = battle_area_rect.left

    def collision(self, direction, collision_sprites):
        """
        Handle collisions with other sprites.

        Parameters
        ----------
        direction: str
            The direction of movement ('horizontal' or 'vertical').
        collision_sprites: pygame.sprite.Group
            Group of sprites to check for collisions.
        """
        for sprite in collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    # Resolve horizontal collision
                    if self.rect.centerx < sprite.rect.centerx:  # Moving right
                        overlap = self.hitbox_rect.right - sprite.rect.left
                        self.rect.x -= overlap
                    elif self.rect.centerx > sprite.rect.centerx:  # Moving left
                        overlap = sprite.rect.right - self.hitbox_rect.left
                        self.rect.x += overlap
                elif direction == 'vertical':
                    # Resolve vertical collision
                    if self.rect.centery < sprite.rect.centery:  # Moving down
                        overlap = self.hitbox_rect.bottom - sprite.rect.top
                        self.rect.y -= overlap
                    elif self.rect.centery > sprite.rect.centery:  # Moving up
                        overlap = sprite.rect.bottom - self.hitbox_rect.top
                        self.rect.y += overlap

                # Sync the hitbox with the rect after collision
                self.hitbox_rect.center = self.rect.center

    def remove_health(self, health_being_removed):
        """
        Remove health from the player if they are not invincible.

        Parameters
        ----------
        health_being_removed: int
            The amount of health removed.
        """
        if not self.invincible:
            if info['health'] >= 0:
                info['health'] -= health_being_removed
            self.health = info['health']

    def get_health(self, amount):  # we should use this if the player picks up hearts or something
        """
        Increase the player's health by a specified amount, up to the maximum health.

        Parameters
        ----------
        amount: int
            The amount of health to be added.
        """
        info['health'] = min(info['health'] + amount, self.max_health)
        self.health = info['health']

    def buy_item(self, item_name):
        """
        Allow the player to buy an item if they have enough gold.

        Parameters
        ----------
        item_name: str
            The name of the item bought.

        """
        # getting the item price from the price_items dictionary
        price = self.price_items[item_name]

        # checking if the player has enough money to buy the item
        if info['gold'] >= price:
            info['gold'] -= price
            coin_music.play()
            info['inventory'][item_name] += 1
            if item_name == 'dog' and self.dog is None:
                self.dog = Dog(self)
                self.dog.bought = True
        else:
            text = pygame.transform.scale(font_for_message.render("Not enough gold!", True, brick_color), (500, 60))
            screen.blit(text, (400, 300))
            pygame.display.update()
            pygame.time.wait(700)

    def add_gold(self, amount):
        """
        Add gold to the player's total gold amount.

        Parameters
        ----------
        amount : int
            The amount of gold to be added.
        """
        info['gold'] += amount
        self.gold = info['gold']

    def give_bonus(self, current_wave):
        """
        Give a bonus item to the player based on the current wave.

        Parameters
        ----------
        current_wave : int
            The current wave number.
        """
        if current_wave == 5:
            info["inventory"]["gold_axe"] += 1
            self.inventory = info["inventory"]
        elif current_wave == 9:
            info["inventory"]["ruby_axe"] += 1
            self.inventory = info["inventory"]
        progress()
