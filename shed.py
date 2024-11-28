from utils import *
from config import resolution, fps, width


def shed(player):
    # setting up the background and the screen
    background = pygame.image.load("images/screens/Giant_Stump.png")
    background = pygame.transform.scale(background, resolution)

    # screen = pygame.display.set_mode(resolution)

    # setting up the clock for fps
    clock = pygame.time.Clock()

    # since I left the previous area from the right, I will start at the left
    player.rect.left = 0

    player_group = pygame.sprite.Group()
    player_group.add(player)

    # setting up the shed area as a special area in the shed map location
    special_area = pygame.Rect(530, 30, 140, 140)

    # normal main game loop (because reasons shed area will not have enemies nor bullets
    # this is our base implementation, and you're allowed to change this

    while True:
        clock.tick(fps)
        screen.blit(background, (0, 0))
        screen.blit(player_score_surf, player_score_rect)

        # allowing the user to quit even tho they shouldn't because our game is perfect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                progress()
                pygame.quit()
                exit()

        # updating player position
        player_group.update()

        # detect if the user walked into the special area (which is the house)
        if special_area.colliderect(player.rect):
            under_construction()

            # changing the player position to the right of the screen
            player.rect.top = 200
            player.rect.left = 560

        # returning to the previous area
        if player.rect.left <= 0:
            player.rect.left = width - player.rect.width

            # switching to the main game
            return "main"

        # drawing the player
        player_group.draw(screen)

        # updating the screen
        pygame.display.flip()
