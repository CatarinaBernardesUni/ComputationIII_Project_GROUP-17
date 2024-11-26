from player import *
from bullet import *
from enemy import *
from config import *
import pygame
from utils import *
from mouse_position import *

# idea is to create mini battles through the game and unlocking new stuff by it

class War:
    def __init__(self, mission_level, reward_type):
        self.mission_level = mission_level
        self.reward_type = reward_type


    def battle(self, player):
        pass