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

# scale all images to the same size
scaled_images_inventory = {item: pygame.transform.scale(image, (50, 50)) for item, image in images_inventory.items()}


# lets the user check their inventory:
def inventory_menu(player):
    on_inventory = True

    # setting up the background image for the inventory
    in_background = pygame.image.load("images/inventory/inventory_board.png").convert_alpha()
    # sets the color black to be transparent. so everywhere around it that was black before is now transparent
    in_background.set_colorkey((0, 0, 0))
    in_background = pygame.transform.scale(in_background, (1000, 300))


    while on_inventory:
        screen.blit(in_background, (width // 2 - 500, height - 300 - 200))

        # setting so my amount of gold appears
        gold_available = inventoryfont.render(f"My Gold: {player.gold}", True, brick_color)
        in_background.blit(gold_available, (width // 2 - 500, height // 2 - 150 - 160))

        # creating the initial position for the 1st item, adapt the others through it
        first_x = width // 2 - 450
        first_y = height // 2
        # creating the item spacing
        item_spacing = 95


        # displaying the items:
        current_x = first_x
        for current_position, (item, count) in enumerate(player.inventory.items()):
            # if the player has at least one item, it appears on inventory
            # blits only the image once. keeps counting after that
            if count > 0:
                item_image = scaled_images_inventory[item]
                # setting the position so its in a single row
                item_x = current_x
                item_y = first_y

                # bliting the images on screen and their amounts
                screen.blit(item_image, (item_x, item_y))

                # setting up the text
                count_text = inventoryfont.render(f"x{count}", True, brick_color)
                # putting the text below the image
                screen.blit(count_text, (item_x, item_y + item_image.get_height() + 5))

                # Update current item position for the next item + the spacing
                current_x += item_image.get_width() + item_spacing

        # handling the key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # exiting the menu with the esc key
                if event.key == pygame.K_ESCAPE:
                    on_inventory = False

        pygame.display.update()
