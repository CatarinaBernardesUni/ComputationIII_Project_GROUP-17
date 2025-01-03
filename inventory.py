from config import *
from mouse_position import draw_button, get_mouse_position, show_hover_message
from mouse_position import get_scaled_mouse_position
from weapon import weapons

# creating a dictionary to store all my pictures for the visual inventory
images_inventory = {'apple': pygame.image.load("images/inventory/apple.png"),
                    'mushroom': pygame.image.load("images/inventory/mushroom.png"),
                    'speed potion': pygame.image.load("images/inventory/potion.png"),
                    'dog': pygame.image.load("images/inventory/doggy.png"),
                    'soup': pygame.image.load("images/inventory/food.png"),
                    'dagger': pygame.image.load("images/weapons/dagger/Moldura 06 (80ms) (replace).png"),
                    'ghost_bow': pygame.image.load("images/inventory/bow.png"),
                    'key': pygame.image.load("images/inventory/key.png"),

                    # weapons not in the store
                    'winter_sword': pygame.image.load("images/weapons/winter_sword/Fundo (80ms).png"),
                    'gold_axe': pygame.image.load("images/weapons/gold_axe/Fundo (110ms).png"),
                    'fire_sword': pygame.image.load("images/weapons/fire_sword/fire01.png"),
                    'ice_bow': pygame.image.load("images/weapons/ice_bow/Moldura 4 (330ms) (replace).png"),
                    'light_bow': pygame.image.load("images/weapons/light_bow/Moldura 4 (170ms) (replace).png"),
                    'ruby_axe': pygame.image.load("images/weapons/ruby_axe/Fundo (80ms).png"),

                    # crystals
                    'red_crystal': pygame.image.load("images/crystals/Dark_red_ crystal2.png"),
                    'blue_crystal': pygame.image.load("images/crystals/Blue_crystal2.png"),
                    'gold_crystal': pygame.image.load("images/crystals/Yellow_crystal2.png"),
                    'purple_crystal': pygame.image.load("images/crystals/Violet_crystal2.png"),
                    'white_crystal': pygame.image.load("images/crystals/White_crystal2.png")
                    }

hover_inventory_messages = {'red_crystal': "Red Crystal: Used to upgrade a dagger to a fire_sword",
                            'blue_crystal': "Blue Crystal: Used to upgrade a dagger to a winter_sword",
                            'gold_crystal': "Gold Crystal: Used to upgrade a ghost_bow to a light_bow",
                            'purple_crystal': "Purple Crystal: Used to increase the damage of any weapon in 20%",
                            'white_crystal': "White Crystal: Used to upgrade a ghost_bow to an ice_bow"

                            }

# scale all images to the same size
scaled_images_inventory = {item: pygame.transform.scale(image, (50, 50)) for item, image in images_inventory.items()}


# lets the user check their inventory:
def inventory_menu(player, place=None, item_type=None):
    """
    Display the inventory menu with optional filtering based on location and item type.

    Parameters
    ----------
    player: Player
        The player object.
    place: str or None
        Optional. Indicates the current location (e.g., "shed").
    item_type: str or None
        Optional. Filters items to display (e.g., "weapons" or "crystals").

    """
    on_inventory = True

    # setting up the background image for the inventory
    in_background = pygame.image.load("images/inventory/inventory_3_floor.png").convert_alpha()
    # sets the color black to be transparent. so everywhere around it that was black before is now transparent
    in_background.set_colorkey((0, 0, 0))
    in_background = pygame.transform.scale(in_background, (1000, 600))

    while on_inventory:
        mouse_pos = pygame.mouse.get_pos()
        scaled_mouse_pos = get_scaled_mouse_position()
        screen.blit(in_background, (width // 2 - 500, height - 650))

        # setting so my amount of gold appears
        gold_available = inventoryfont.render(f"My Gold: {info['gold']}", True, brick_color)
        in_background.blit(gold_available, (width // 2 - 500, height // 2 - 320))

        # creating the initial position for the 1st item, adapt the others through it
        first_x = width // 2 - 450
        first_y = height // 2 - 180
        # creating the item spacing
        item_spacing = 90
        row_spacing = 120

        # storing each one of the items position and dimensions so i can use it later
        item_positions = []

        # limit the number of items per row
        items_per_row = 7

        filtered_items = get_filtered_items(player, place, item_type)
        display_items(screen, filtered_items, item_positions, first_x, first_y, item_spacing, row_spacing,
                      items_per_row)
        # drawing the inventory button
        inventory_button = draw_button(display, 550, y=10, width_of_button=70, height_of_button=35,
                                       text="Inventory",
                                       text_color=brick_color, image_path="images/buttons/basic_button.png",
                                       font=cutefont)
        # Detect hover and show messages
        for item_name, item_x, item_y, item_width, item_height in item_positions:
            item_rect = pygame.Rect(item_x, item_y, item_width, item_height)
            if item_rect.collidepoint(mouse_pos):
                if item_name in hover_inventory_messages:
                    show_hover_message(screen, mouse_pos, item_rect, hover_inventory_messages[item_name], True)

                else:
                    weapon_data = weapons.get(item_name)
                    if weapon_data:
                        damage = info["weapon_attributes_evolved"][item_name]
                        description = f"{item_name.capitalize()} - Damage: {damage}, Tier: {weapon_data['tier']}"
                        show_hover_message(screen, mouse_pos, item_rect, description, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    on_inventory = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if inventory_button.collidepoint(scaled_mouse_pos):
                    on_inventory = False
                selected_item = handle_item_click(item_positions)
                if selected_item:
                    if place == "shed":
                        return selected_item
                    else:
                        # Handle general inventory interactions
                        if not any(weapon in selected_item for weapon in ["sword", "bow", "axe", "dagger"]):
                            info['inventory'][selected_item] -= 1
                        sparkly_music.play()
                        if selected_item in player.health_boosts.keys():
                            player.get_health(player.health_boosts[selected_item])
                        if any(weapon in selected_item for weapon in ["sword", "bow", "axe", "dagger"]):
                            if "sword" in selected_item or "dagger" in selected_item:
                                player.switch_weapon(selected_item, "Sword")
                            elif "bow" in selected_item:
                                player.switch_weapon(selected_item, "Bow")
                            elif "axe" in selected_item:
                                player.switch_weapon(selected_item, "Axe")
                        progress()

            pygame.display.flip()


def get_filtered_items(player, place=None, item_type=None):
    """
    Filters and retrieves items from a player's inventory or a specific place.

    Parameters
    ----------
    player : Player
        An object representing the player, which has an `inventory` attribute (a dictionary of item names and counts).
    place : str, optional
        The location to filter items from (default is None). If "shed", items will be filtered based on `item_type`.
    item_type : str, optional
        The type of items to filter when `place` is "shed" (default is None). Supported values are:
        - "weapons": Filters items containing "sword", "bow", "axe", or "dagger".
        - "crystals": Filters items containing "crystal".

    Returns
    -------
    dict
        A dictionary of filtered items, where keys are item names, and values are their counts. The filtering criteria
        depend on the `place` and `item_type` parameters:
        - When `place` is "shed":
            - If `item_type` is "weapons", returns items classified as weapons.
            - If `item_type` is "crystals", returns items classified as crystals.
        - Otherwise, returns all items in the player's inventory except "dog".
    """

    if place == "shed":
        if item_type == "weapons":
            return {name: info["inventory"][name] for name in info["inventory"] if
                    info["inventory"].get(name, 0) > 0 and any(weapon in name for weapon in ["sword", "bow",
                                                                                             "axe", "dagger"])}
        elif item_type == "crystals":
            return {name: info["inventory"][name] for name in info["inventory"] if
                    info["inventory"].get(name, 0) > 0 and "crystal" in name}
    return {item: count for item, count in player.inventory.items() if item != "dog"}


def display_items(screen, filtered_items, positions, first_x, first_y, item_spacing, row_spacing, items_per_row):
    """
    Display items on the screen and store their positions for later interaction.

    Parameters
    ----------
    screen: pygame.Surface
        The game screen.
    filtered_items: dict
        dictionary of items to display with their counts.
    positions: list
        to store the positions of displayed items.
    first_x: int
        starting x-coordinate.
    first_y: int
        starting y-coordinate.
    item_spacing: int
        Horizontal spacing between items.
    row_spacing: int
        Vertical spacing between rows of items.
    items_per_row: int
        Maximum number of items per row.

    """
    current_x, current_y = first_x, first_y
    for item_name, count in filtered_items.items():
        if count > 0:
            item_image = scaled_images_inventory[item_name]
            # Draw the item image at the current position on the screen
            screen.blit(item_image, (current_x, current_y))
            # count the items
            count_text = inventoryfont.render(f"x{count}", True, brick_color)
            screen.blit(count_text, (current_x, current_y + item_image.get_height() + 5))

            positions.append((item_name, current_x, current_y, item_image.get_width(), item_image.get_height()))
            current_x += item_image.get_width() + item_spacing

            # If the current row is full, reset x-coordinate and move to the next row
            if len(positions) % items_per_row == 0:
                current_x = first_x
                current_y += item_image.get_height() + row_spacing

def handle_item_click(positions):
    """
    Handle item selection on mouse click.

    Parameters
    ----------
    positions: list
         item positions and dimensions.

    Returns
    -----------
    The name of the selected item, if any.

    """
    mouse_x, mouse_y = get_mouse_position()
    for item_name, item_x, item_y, item_width, item_height in positions:
        if item_x <= mouse_x <= item_x + item_width and item_y <= mouse_y <= item_y + item_height:
            return item_name
    return None
