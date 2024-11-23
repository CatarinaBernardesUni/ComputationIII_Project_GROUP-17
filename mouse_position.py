import pygame

def get_mouse_position():
    return pygame.mouse.get_pos()

# drawing a button, just skeleton does not work on its own:
def draw_button(screen, x, y, width, height, text, text_color, button_color):
    # setting up font and text for going back
    corbelfont = pygame.font.SysFont("Corbel", 50)
    back_text = corbelfont.render(text, True, text_color)
    # drawing the back button
    pygame.draw.rect(screen, button_color, [x, y, width, height])
    back_rect = back_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(back_text, back_rect)
    # returning my button
    return pygame.Rect(x, y, width, height)

# drawing the function that will make the back button work:
def activate_back_button(screen, background, x, y, width, height, text, tex_color, button_color):
    while True:
        # getting the mouse position
        mouse = get_mouse_position()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                back_button_rect = draw_button(screen=screen, x=x, y=y, width=width, height=height, text=text, text_color=tex_color, button_color=button_color)
                if back_button_rect.collidepoint(mouse):
                    return   # return from where it was before

        # displaying the background
        screen.blit(background, (0, 0))

        # drawing the button
        draw_button(screen=screen, x=x, y=y, width=width, height=height, text=text, text_color=tex_color, button_color=button_color)

        # Updating our screen
        pygame.display.update()
