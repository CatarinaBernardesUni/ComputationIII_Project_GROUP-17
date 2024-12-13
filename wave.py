import random
import pygame

from enemy import Enemy


class WaveManager:
    def __init__(self, player, sprite_group, enemies, battle_area_rect):
        self.current_wave = 0
        self.battle_area_rect = battle_area_rect
        self.enemies = enemies
        self.sprite_group = sprite_group #todo: check if this attribute is really necessary
        self.player = player
        self.active_enemies = pygame.sprite.Group()

        self.predefined_waves = [
            {"green_slime": 3},  # Wave 1: 3 green_slimes
            {"green_slime": 5, "normal_fly": 2},  # Wave 2: 5 green_slimes, 2 normal_flies
            {"normal_fly": 5, "fire_fly": 3},  # Wave 3: 5 normal_flies, 3 fire_flies
            {"fire_fly": 4, "horse_ghost": 1},  # Wave 4: 4 fire_flies, 1 horse_ghost
            {"horse_ghost": 3, "electric_fly": 2},  # Wave 5: 3 horse_ghosts, 2 electric_flies
            {"electric_fly": 4, "myst_ghost": 1},  # Wave 6: 4 electric_flies, 1 myst_ghost
            {"myst_ghost": 2, "electric_enemy": 1},  # Wave 7: 2 myst_ghosts, 1 electric_enemy
            {"electric_enemy": 3, "myst_ghost": 2},  # Wave 8: 3 electric_enemies, 2 myst_ghosts
        ] # todo: change this amounts to be more balanced

    def start_next_wave(self):
        self.current_wave += 1
        print(f"Wave {self.current_wave} starting!") #todo: print this in a balloon on the screen

        # there are 8 predefined waves, if we are out of them, generate a random wave
        if self.current_wave <= len(self.predefined_waves):
            wave_config = self.predefined_waves[self.current_wave - 1]
        else:
            wave_config = self.generate_random_wave()

        self.spawn_wave(wave_config)

    def spawn_wave(self, wave_config):
        for enemy_name, count in wave_config.items():
            for _ in range(count):
                # Spawn the enemy
                enemy = Enemy(self.player, self.sprite_group, enemy_name, self.player, self.battle_area_rect)
                self.active_enemies.add(enemy)
                self.active_enemies.update()

    #def generate_random_wave(self):
        # the more waves you do the bigger they become
        # todo: introduce a stopping point
        #num_enemies = 3 + int(self.current_wave ** 1.2)

        # Generate a random wave configuration
        #wave_config = {}
        #for i in range(num_enemies):
            #chosen_enemy = random.choices(possible_enemies, weights=weights, k=1)[0]
            #wave_config[chosen_enemy] = wave_config.get(chosen_enemy, 0) + 1

        #return wave_config

    def update(self):
        # Check if all enemies are defeated
        if not self.active_enemies:
            print(f"Wave {self.current_wave} completed!")
            self.reward_player()
            # todo: introduce a condition to start the next wave
            self.start_next_wave()

    def reward_player(self):
        print(f"Player receives a reward for completing wave {self.current_wave}!")
        self.player.gold += 50
        if random.random() < 0.3:
            pass

# todo: make a function that detects if an enemy died and has a percentage of dropping a reward