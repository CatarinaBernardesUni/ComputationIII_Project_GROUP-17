from config import *


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = power_up_invincibility
        self.rect = self.image.get_rect

    def affect_player(self, power_up_name):
        if power_up_name == "invincibility":
            self.image = power_up_invincibility
        if power_up_name == "speed":
            self.image = power_up_speed

    def affect_game(self, power_up_name):
        if power_up_name == "de_spawner":
            self.image = power_up_de_spawner

    def show(self):
        pass


class Invincibility(PowerUp):
    def __init__(self):
        super().__init__()


class Speed(PowerUp):
    def __init__(self):
        super().__init__()


class De_Spawner(PowerUp):
    def __init__(self):
        super().__init__()
