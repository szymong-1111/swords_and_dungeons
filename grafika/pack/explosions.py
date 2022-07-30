import pygame
from pygame import mixer
pygame.init()

clock = pygame.time.Clock()

explosion_list = list()
hitbox_list = list()


def explosion(x, y):
    global explosion_list
    global hitbox_list

    explosion_sound = mixer.Sound('explosion.wav')
    explosion_sound.play()

    explosion_list.append((x, y))
    explosion_list.append((x + 80, y))
    explosion_list.append((x - 80, y))
    explosion_list.append((x, y + 80))
    explosion_list.append((x, y - 80))

    hitbox_list.append(pygame.Rect(x, y, 80, 80))
    hitbox_list.append(pygame.Rect(x+80, y, 80, 80))
    hitbox_list.append(pygame.Rect(x-80, y, 80, 80))
    hitbox_list.append(pygame.Rect(x, y+80, 80, 80))
    hitbox_list.append(pygame.Rect(x, y-80, 80, 80))


def explode(explosion_counter, screen, npcs, player):
    global explosion_list
    global hitbox_list

    if explosion_counter <= 1:
        for hitbox in hitbox_list:
            for npc in npcs:
                if pygame.Rect.colliderect(npc.rect, hitbox):
                    npc.hp -= 10
            if pygame.Rect.colliderect(player.rect, hitbox):
                player.hp -= 10

    explosion_img = pygame.image.load('explosion_demo.png').convert_alpha()
    if explosion_counter <= 10:
        for explosion in explosion_list:
            screen.blit(explosion_img, explosion)
            explosion_counter += 1
        return explosion_counter
    else:
        explosion_list.clear()
        hitbox_list.clear()
        return 0








