from player import Player
import pygame
from config import *
from store import shop_menu
from mouse_position import draw_button, get_mouse_position

# creating a dictionary to store all my pictures for the visual inventory
images_inventory = {
                      'apple': pygame.image.load("images/inventory/apple.png"),
                      'mushroom': pygame.image.load("images/inventory/mushroom.png"),
                      'speed potion': pygame.image.load("images/inventory/potion.png"),
                      'dog': pygame.image.load("images/inventory/doggy.png"),
                      'soup': pygame.image.load("images/inventory/food.png"),
                      'sword': pygame.image.load("images/inventory/sword.png"),
                      'bow': pygame.image.load("images/inventory/bow.png"),
                      'key': pygame.image.load("images/inventory/key.png")
                    }

# lets the user check their inventory:
def inventory_menu(player):
    on_inventory = True
    while on_inventory:
        screen.blit("images/store/board.png", (0, 0))
        for event in pygame.event.get():
            mouse = get_mouse_position()
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            pygame.display.update()
        pygame.display.update()
