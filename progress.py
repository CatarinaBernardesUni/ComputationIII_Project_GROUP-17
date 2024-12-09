import json
import pygame

pygame.init()

pixel = pygame.font.SysFont("Pixel", 50, 9)
info = {"health": 5, "score": 0, "coins": 0}

try:
    with open("player_info.txt") as player_file:
        info = json.load(player_file)
except:
    print('no file created yet.')

<<<<<<< HEAD

# player_score_surf = pixel.render(f"score: {info['score']}", True, "black")
# player_score_rect = player_score_surf.get_rect(center=(65, 55))
=======
player_score_surf = pixel.render(f"score: {info['score']}", True, "black")
player_score_rect = player_score_surf.get_rect(center=(80, 80))
>>>>>>> parent of 007b198 (test)
