import pygame



# Function to draw a stick figure with a construction hat
def draw_stick_figure_with_hat(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg

    # hat
    hat_color = (255, 215, 0)

    # drawing the construction hat
    pygame.draw.rect(screen, hat_color, [x - 25, y - 30, 50, 10])  # Hat's brim
    pygame.draw.rect(screen, hat_color, [x - 20, y - 40, 40, 20])  # Hat's dome


# Function to draw a normal stick figure (without a hat)
def draw_normal_stick_figure(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2)  # Left arm
    pygame.draw.line(screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2)  # Right arm

    # legs
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2)  # Left leg
    pygame.draw.line(screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2)  # Right leg