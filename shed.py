from config import *
from utils import *
from visual import *


# the second background
def shed(player):
    # setting up the background and the screen
    background = pygame.image.load("images/village.jpg")

    # scaling the background image into our selected resolution
    background = pygame.transform.scale(background, resolution)

    # placing my house on the screen
    house = House(width=190, height=250, visual_path="images/outside_house.png")
    house.set_position(160, 120)

    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    # setting up a clock for fps
    clock = pygame.time.Clock()

    # since I left the previous area from the right, here I begin on the left
    player.rect.left = 0

    # creating the player group
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # setting up the shed area as a special area in the shed map location
    special_area = pygame.Rect(530, 30, 140, 140)

    # normal main game loop (because reasons, shed area will not have enemies nor bullets)
    # this is our base implementation and you're allowed to change this!!!
    # todo: create several areas that player can go to

    running = True

    while running:
        clock.tick(fps)
        # displaying the farm background on the entirety of the screen
        screen.blit(background, (0, 0))
        screen.blit(house.visual_image, house.detect_coll)

        # allowing the user to quit even tho they shouldn't because our game is perfect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # updating player position
        player.update()

        # detect if the user walked in to the special area (which is the house)
        if special_area.colliderect(player.rect):
            under_construction()

            # changing the players position
            player.rect.top = 200
            player.rect.left = 560

        # allowing the player to return back to the previous area/screen
        if player.rect.left <= 0:
            # position the player to the right of the screen
            player.rect.left = width - player.rect.width

            # switching back to the main game:
            return "main"

        # drawing the player
        player_group.draw(screen)

        # updating the screen
        pygame.display.flip()
        