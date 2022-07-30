import pygame

pygame.init()


def print_on_screen(text_to_show, screen, x, y, font_size=16, color=(255, 255, 255)):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(text_to_show, True, color)
    screen.blit(text, (x, y))
