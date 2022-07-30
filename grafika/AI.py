#from algorithm import paths
import pygame
import random
import math

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
        if path_to_go == player.last_target:
            if len(available_paths) > 1:
                available_paths.remove(path_to_go)
                path_to_go = random.choice(available_paths)

        return path_to_go
    else:
        return 0


def seek_and_destroy(player, paths, target):
    available_paths = list()
    for path in paths:
        if [player.x+32, player.y+40] == path[0]:
            available_paths.append(path[1])
        elif [player.x+32, player.y+40] == path[1]:
            available_paths.append(path[0])

    if available_paths:
        distances = dict()
        counter = 0
        for way in available_paths:
            d = math.sqrt((way[0] - (target.x+32)) ** 2 + (way[1] - (target.y+32)) ** 2)
            distances.update({d: counter})
            counter += 1

        return available_paths[distances[min(distances)]]


def find_path(player, paths):
    distances = dict()
    for path in paths:
        d = math.sqrt((path[0][0] - (player.x + 32)) ** 2 + (path[0][1] - (player.y + 32)) ** 2)
        d1 = math.sqrt((path[1][0] - (player.x + 32)) ** 2 + (path[1][1] - (player.y + 32)) ** 2)

        distances.update({d: path[0]})
        distances.update({d1: path[1]})

    return distances[min(distances)]











