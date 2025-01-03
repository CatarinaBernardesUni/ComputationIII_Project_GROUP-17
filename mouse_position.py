from config import *


def get_mouse_position():
    """
    Gets the current mouse position.
    Created to be more efficient.

    Returns
    -----------
    tuple
        the current mouse position as a tuple (x, y)

    """
    return pygame.mouse.get_pos()


def get_scaled_mouse_position():
    """
    Gets the current mouse position and scales it down by 2.

    Returns
    -----------
    tuple
        the scaled mouse position
    """
    mouse_pos = pygame.mouse.get_pos()
    scaled_mouse_pos = (mouse_pos[0] // 2, mouse_pos[1] // 2)
    return scaled_mouse_pos


# drawing a button, just skeleton does not work on its own:
def draw_button(screen, x, y, width_of_button, height_of_button, text, text_color, image_path, font):
    """
    Draws a button on the screen with the user's desired definitions, such as size, image, font, text color, etc.

    Parameters
    ----------
    screen: pygame.Surface
        The surface where the button will be drawn on.
    x: float
        The x-coordinate of the button's top-left corner.
    y: float
        The y-coordinate of the button's top-left corner.
    width_of_button: int
        The width of the button.
    height_of_button: int
        The height of the button.
    text: str
        The text that should be displayed on the button.
    text_color: rgb tuple
        The color the text will be displayed in.
    image_path: str
        The file path to the button's image.
    font: pygame.font.Font
        The font to use for the button's text.

    Returns
    -----------
    pygame.Rect
        The rectangle representing the button's position and size

    """

    button_image = pygame.image.load(image_path).convert_alpha()  # making sure that it handles transparency
    button_image = pygame.transform.scale(button_image, (width_of_button, height_of_button))

    # Blit the button image onto the screen
    screen.blit(button_image, (x, y))

    # setting up font and text for going back
    text_surface = font.render(text, False, text_color)
    text_rect = text_surface.get_rect(center=(x + width_of_button // 2, y + height_of_button // 2))
    screen.blit(text_surface, text_rect)
    # returning my button
    return pygame.Rect(x, y, width_of_button, height_of_button)


# make a message appear when hover over my rectangles
# help: https://stackoverflow.com/questions/69833827/how-do-i-make-a-text-box-pop-up-when-i-hover-over-a-button-in-pygame
def show_hover_message(screen, mouse_pos, button_rect, description, on_inventory=False):
    """
    Shows a message when the mouse is over a button.
    Relates an object of the store to its description such as price and its utilization.

    Parameters
    ----------
    screen: pygame.Surface
        the screen where the hover message will be displayed
    mouse_pos: tuple (x, y)
        receives the mouse position.
    button_rect: pygame.Rect
        receives the rectangle representing the button's position and size
    description: str
        receives a string as the description that needs to appear when hover message.
    on_inventory: boolean
        determines if the hover message is for an inventory item (default as False)
    """
    custom_font = pygame.font.Font("fonts/Minecraft.ttf", 20)
    tip_surface = custom_font.render(description, True, white)

    background_width = tip_surface.get_width() + 10
    background_height = tip_surface.get_height() + 10
    background_surface = pygame.Surface((background_width, background_height), pygame.SRCALPHA)
    pygame.draw.rect(background_surface, brick_color_transparent, background_surface.get_rect(),
                     border_radius=5)  # rounded rectangle

    if button_rect.collidepoint(mouse_pos):
        if not on_inventory:
            # Blit the text onto the background surface
            # creates a small padding for the text of 5
            background_surface.blit(tip_surface, (5, 5))

            screen.blit(background_surface, (mouse_pos[0] + 16, mouse_pos[1]))
        else:
            # Blit the text onto the background surface
            text_padding = 5
            background_surface.blit(tip_surface, (text_padding, text_padding))

            # Positioning the hover message
            hover_x = mouse_pos[0] + 16
            hover_y = mouse_pos[1] + button_rect.height + 5  # Position below the image

            # Constrain the position within the defined limits for a 640px screen
            if 640 <= pygame.display.get_surface().get_width():  # Check if screen width is 640
                hover_x = max(250, min(hover_x, 390))

            # Adjusting hover position if it exceeds screen bounds
            if hover_x + background_width > pygame.display.get_surface().get_width():
                hover_x = pygame.display.get_surface().get_width() - background_width - 10

            if hover_y + background_height > pygame.display.get_surface().get_height():
                hover_y = pygame.display.get_surface().get_height() - background_height - 10

            # Blit the background and text onto the screen
            screen.blit(background_surface, (hover_x, hover_y))


button_data = {
    "apple": {"rect": pygame.Rect(348, 291, 97, 43),
              "description": "30 gold. A delicious apple that restores 1 heart."},
    "mushroom": {"rect": pygame.Rect(509, 291, 96, 43), "description": "50 gold. A mushroom that restores 2 hearts."},
    "speed potion": {"rect": pygame.Rect(670, 291, 96, 43),
                     "description": "70 gold. A potion that increases your speed."},
    "dagger": {"rect": pygame.Rect(834, 291, 96, 43), "description": "100 gold. A sword to defend yourself."},
    "dog": {"rect": pygame.Rect(347, 503, 97, 43), "description": "200 gold. A dog companion for the journey."},
    "soup": {"rect": pygame.Rect(499, 503, 101, 43), "description": "100 gold. A bowl of soup that restores 5 hearts."},
    "ghost_bow": {"rect": pygame.Rect(673, 503, 94, 43), "description": "200 gold. A bow for ranged attacks."},
    "key": {"rect": pygame.Rect(832, 500, 94, 43), "description": "300 gold. A key to unlock special things."}
}
