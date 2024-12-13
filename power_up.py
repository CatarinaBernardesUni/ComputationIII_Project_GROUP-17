from config import *


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = power_up_invincibility
        self.rect = self.image.get_rect

    def affect_player(self):
        pass

    def affect_game(self):
        pass

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
