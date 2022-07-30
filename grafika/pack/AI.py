#from algorithm import paths
import pygame
import random

pygame.init()


def follow_path(player, paths):
    available_paths = list()
    for path in paths:
        if [player.x+32, player.y+40] == path[0]:
            available_paths.append(path[1])
        elif [player.x+32, player.y+40] == path[1]:
            available_paths.append(path[0])

    if available_paths:
        path_to_go = random.choice(available_paths)
        return path_to_go
    else:
        return 0








