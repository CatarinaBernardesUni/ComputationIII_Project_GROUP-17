from config import *


class Power_up(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None

    def affect_player(self, power_up_name):
        if power_up_name == "invincibility":
            self.image = power_up_invincibility
        if power_up_name == "speed":
            self.image = power_up_speed

    def affect_game(self, power_up_name):
        if power_up_name == "de_spawner":
            self.image = power_up_de_spawner
