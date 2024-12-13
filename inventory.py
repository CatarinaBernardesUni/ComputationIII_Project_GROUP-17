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
    in_background = pygame.image.load("images/inventory/inventory_2_floor.png").convert_alpha()
    # sets the color black to be transparent. so everywhere around it that was black before is now transparent
    in_background.set_colorkey((0, 0, 0))
    in_background = pygame.transform.scale(in_background, (1000, 450))


    while on_inventory:
        screen.blit(in_background, (width // 2 - 500, height - 350 - 200))

        # setting so my amount of gold appears
        gold_available = inventoryfont.render(f"My Gold: {player.gold}", True, brick_color)
        in_background.blit(gold_available, (width // 2 - 500, height // 2 - 150 - 160))

        # creating the initial position for the 1st item, adapt the others through it
        first_x = width // 2 - 450
        first_y = height // 2 - 70
        # creating the item spacing
        item_spacing = 95
        row_spacing = 130

        # storing each one of the items position and dimensions so i can use it later
        item_positions = []

        # getting their positions
        current_x = first_x
        current_y = first_y

        # limit the number of items per row
        items_per_row = 7
        item_count = 0

        # displaying the items:
        for current_position, (item, count) in enumerate(player.inventory.items()):
            # Skip the dog item, dont want it to appear as a part of the inventory
            # cant take the dog back!!!!
            if item == 'dog':
                continue

            # if the player has at least one item, it appears on inventory
            # blits only the image once. keeps counting after that
            if count > 0:
                item_image = scaled_images_inventory[item]
                # setting the position so its in a single row
                item_x = current_x
                item_y = current_y

                # bliting the images on screen and their amounts
                screen.blit(item_image, (item_x, item_y))
                count_text = inventoryfont.render(f"x{count}", True, brick_color)
                screen.blit(count_text, (item_x, item_y + item_image.get_height() + 5))

                # store the item position and dimensions
                item_positions.append((item, item_x, item_y, item_image.get_width(), item_image.get_height()))

                # Update current item position for the next item + the spacing
                current_x += item_image.get_width() + item_spacing
                item_count += 1

                # move to next row if first row complete > 7:
                # ensures all multiples of 7 are 0, so it changes row
                # 14 % 7 = 0 so creates a 3rd line
                if item_count % items_per_row == 0:
                    current_x = first_x
                    current_y += item_image.get_height() + row_spacing

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
            # being able to select my items for further utilization
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = get_mouse_position()
                # check if the click is within any item bounds
                for item, item_x, item_y, item_width, item_height in item_positions:
                    if item_x <= mouse_x <= item_x + item_width and item_y <= mouse_y <= item_y + item_height:
                        # handle item usage
                        print(f"it is working {item}")


        pygame.display.update()