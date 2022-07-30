import math
import random
import pygame

pygame.init()
#screen = pygame.display.set_mode((800, 600))
everything = []

player = pygame.Rect(400, 300, 64, 64)
clock1 = pygame.time.Clock()


class Builder:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 'right'

    def display(self, screen):
        self.rect.update(self.x, self.y, self.width, self.height)
        new_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), new_rect)
        everything.append(new_rect)

    def move(self):
        if self.direction == 'right':
            self.x += 64
        elif self.direction == 'left':
            self.x -= 64
        elif self.direction == 'up':
            self.y -= 64
        elif self.direction == 'down':
            self.y += 64


class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self, screen):
        self.rect.update(builder.x, builder.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        everything.append(self.rect)


builder = Builder(0, 300)


def generate_dungeon(screen):
    building = True
    while building:
        builder.direction = 'right'
        for _ in range(random.randint(2, 3)):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        builder.direction = random.choice(('up', 'down'))

        for _ in range(3):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        room = Room(builder.x, builder.y, random.randint(128, 256), random.randint(128, 256))
        if builder.direction == 'up':
            builder.y -= room.height-64
            builder.x -= room.width/2 - 32
            room.display(screen)
            builder.y += room.height-64
            builder.direction = 'down'
        else:
            builder.x -= room.width/2 - 32
            room.display(screen)
            builder.direction = 'up'

        builder.x += room.width/2 - 32

        for _ in range(3):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        print(room.width, room.height)
        pygame.display.update()

        if builder.x >= 1400:
            building = False

    while True:
        builder.x = 0
        builder.y = 0
        builder.display(screen)
        builder.direction = 'down'
        builder.move()

        builder.direction = 'right'
        builder.move()
        while builder.y >= 600:
            builder.direction = 'up'
            builder.display()
            builder.move()

#generate_dungeon(screen)

'''running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.right += 10
            if event.key == pygame.K_LEFT:
                screen.fill((0, 0, 0))
                for thing in everything:
                    thing.x += 64
                    pygame.draw.rect(screen, (255, 255, 255), thing)
            if event.key == pygame.K_UP:
                screen.fill((0, 0, 0))
                for thing in everything:
                    thing.y += 64
                    pygame.draw.rect(screen, (255, 255, 255), thing)
            if event.key == pygame.K_DOWN:
                screen.fill((0, 0, 0))
                for thing in everything:
                    thing.y -= 64
                    pygame.draw.rect(screen, (255, 255, 255), thing)

    pygame.draw.rect(screen, (255, 0, 0), player)

    pygame.display.update()'''

clock1.tick(60)

