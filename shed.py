from utils import *
from config import resolution, fps, width

def battle_area(player):
    # setting up the background and the screen
    background = pygame.image.load("images/screens/Giant_Stump.png")
    background = pygame.transform.scale(background, resolution)

    # setting up the screen
    screen = pygame.display.set_mode(resolution)

    # setting up a clock for fps
    clock = pygame.time.Clock()

    # since I left the previous area from the right, here I begin on the left
    player.rect.left = 0

    # creating the player group
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # normal main game loop (because reasons, shed area will not have enemies nor bullets)
    # this is our base implementation and you're allowed to change this!!!
    # todo: create several areas that player can go to

    # normal main game loop (because reasons shed area will not have enemies nor bullets
    # this is our base implementation, and you're allowed to change this

    running = True

    while True:
        clock.tick(fps)
        # displaying the farm background on the entirety of the screen and the house
        screen.blit(background, (0, 0))

        screen.blit(player_score_surf, player_score_rect)

        # allowing the user to quit even tho they shouldn't because our game is perfect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()

        # updating player position
        player.update()

        # allowing the player to return back to the previous area/screen from area 2 to area 1
        if player.rect.left <= 0:
            # position the player to the right of the screen
            player.rect.left = width - player.rect.width

            # switching back to the main game:
            return "main"

        # drawing the player
        player_group.draw(screen)

        # updating the screen
        pygame.display.flip()
