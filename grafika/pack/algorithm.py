from pygame import mixer
import random
import pygame

pygame.init()
#screen = pygame.display.set_mode((800, 600))
everything = []
walls = []
spawnpoints = []
paths = []

player = pygame.Rect(400, 300, 64, 64)
clock1 = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)
text = font.render('generating stage...', True, (255, 255, 255))


def build_room(screen, builder):
    height = random.randint(1, 3)
    width = random.randint(1, 2)
    start_point = [builder.x + 40, builder.y + 40]

    builder.display(screen)
    builder.move()
    builder.display(screen)

    paths.append((start_point, [builder.x + 40, builder.y + 40]))
    start_point = [builder.x + 40, builder.y + 40]

    four_directions = ['right', 'down', 'left', 'up']

    for _ in range(2):
        for _ in range(height):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        try:
            builder.direction = four_directions[four_directions.index(builder.direction)+1]
        except IndexError:
            builder.direction = four_directions[0]

        spawnpoints.append([start_point[0] - 32, start_point[1] - 40])

        paths.append((start_point, [builder.x + 40, builder.y + 40]))
        start_point = [builder.x + 40, builder.y + 40]

        for _ in range(width):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        try:
            builder.direction = four_directions[four_directions.index(builder.direction) + 1]
        except IndexError:
            builder.direction = four_directions[0]

        spawnpoints.append([start_point[0] - 32, start_point[1] - 40])

        paths.append((start_point, [builder.x + 40, builder.y + 40]))
        start_point = [builder.x + 40, builder.y + 40]

    try:
        builder.direction = four_directions[four_directions.index(builder.direction) - 1]
    except IndexError:
        builder.direction = four_directions[-1]

    spawnpoints.append([start_point[0] - 32, start_point[1] - 40])

    for _ in range(2):
        for _ in range(width):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        try:
            builder.direction = four_directions[four_directions.index(builder.direction)+1]
        except IndexError:
            builder.direction = four_directions[0]

        paths.append((start_point, [builder.x + 40, builder.y + 40]))
        start_point = [builder.x + 40, builder.y + 40]

        for _ in range(height):
            builder.display(screen)
            builder.move()
            builder.display(screen)

        try:
            builder.direction = four_directions[four_directions.index(builder.direction) + 1]
        except IndexError:
            builder.direction = four_directions[0]

        spawnpoints.append([start_point[0] - 32, start_point[1] - 40])

        paths.append((start_point, [builder.x + 40, builder.y + 40]))
        start_point = [builder.x + 40, builder.y + 40]

    try:
        builder.direction = four_directions[four_directions.index(builder.direction) + 1]
    except IndexError:
        builder.direction = four_directions[0]

    builder.display(screen)
    builder.move()
    builder.display(screen)

    paths.append((start_point, [builder.x + 40, builder.y + 40]))
    # start_point = [builder.x + 40, builder.y + 40]


class Builder:
    def __init__(self, x, y, colors=(0, 0, 0), structure_type='room'):
        self.x = x
        self.y = y
        self.structure_type = structure_type
        if self.structure_type == 'wall':
            self.width = 40
            self.height = 40
        else:
            self.width = 80
            self.height = 80
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 'right'
        self.colors = colors

    def display(self, screen):
        self.rect.update(self.x, self.y, self.width, self.height)
        new_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.structure_type == 'room':
            everything.append(new_rect)
        else:
            walls.append(new_rect)

    def move(self):
        if self.structure_type == 'wall':
            if self.direction == 'right':
                self.x += 40
            elif self.direction == 'left':
                self.x -= 40
            elif self.direction == 'up':
                self.y -= 40
            elif self.direction == 'down':
                self.y += 40

        else:
            if self.direction == 'right':
                self.x += 80
            elif self.direction == 'left':
                self.x -= 80
            elif self.direction == 'up':
                self.y -= 80
            elif self.direction == 'down':
                self.y += 80


def build_walls(screen):
    wall = Builder(-40, 540, colors=(50, 50, 50), structure_type='wall')
    building = True
    wall.direction = 'up'
    while building:
        wall.display(screen)
        wall.move()
        if wall.y <= -2400:
            wall.direction = 'right'
            wall.display(screen)
            wall.move()
            wall.direction = 'down'
        if wall.y >= 1200:
            wall.direction = 'right'
            wall.display(screen)
            wall.move()
            wall.direction = 'up'
        if wall.x >= 2400:
            building = False


def generate_dungeon(screen):

    go_down_sound = mixer.Sound('go_down.wav')
    go_down_sound.play()

    builder = Builder(0, 300)
    print(builder.x)
    for _ in range(2):
        building = True
        start_point = [builder.x+40, builder.y+40]
        while building:
            builder.direction = 'right'
            for _ in range(random.randint(2, 3)):
                builder.display(screen)
                builder.move()
                builder.display(screen)

            paths.append((start_point, [builder.x+40, builder.y+40]))
            start_point = [builder.x+40, builder.y+40]

            builder.direction = random.choice(('up', 'down'))

            for _ in range(2):
                builder.display(screen)
                builder.move()
                builder.display(screen)

            build_room(screen, builder)

            if builder.direction == 'up':
                builder.direction = 'down'
            else:
                builder.direction = 'up'

            for _ in range(2):
                builder.display(screen)
                builder.move()
                builder.display(screen)

            paths.append((start_point, [builder.x+40, builder.y+40]))
            start_point = [builder.x+40, builder.y+40]

            builder.display(screen)
            builder.move()
            builder.display(screen)

            paths.append((start_point, [builder.x+40, builder.y+40]))
            start_point = [builder.x+40, builder.y+40]

            screen.fill((0, 0, 0))
            screen.blit(text, (300, 250))
            pygame.display.update()

            if builder.x >= 1314:
                building = False

        builder.y = -180  # 640
        builder.x = 0


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

