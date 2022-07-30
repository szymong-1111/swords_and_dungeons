import pygame


pygame.init()

window = pygame.display.set_mode((400, 200))


# TITLE AND ICON
pygame.display.set_caption('Swords and Dungeons')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


select_frame = pygame.image.load('select_frame.png')
show_select_frame = False

font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 16)


def show_text():
    text = font.render('CHOOSE YOUR CLASS', True, (255, 255, 255))
    wiz = small_font.render('wizard', True, (255, 255, 255))
    kng = small_font.render('knight', True, (255, 255, 255))
    rge = small_font.render('rogue', True, (255, 255, 255))

    window.blit(text, (20, 30))
    window.blit(wiz, (55, 150))
    window.blit(kng, (180, 150))
    window.blit(rge, (305, 150))


knight = pygame.image.load('knight.png')
wizard = pygame.image.load('wizard.png')
rogue = pygame.image.load('rogue.png')

knight_rect = pygame.Rect(175, 75, 64, 64)
wizard_rect = pygame.Rect(50, 75, 64, 64)
rogue_rect = pygame.Rect(300, 75, 64, 64)


def display_characters():

    window.blit(knight, (175, 75))
    window.blit(wizard, (50, 75))
    window.blit(rogue, (300, 75))


which_character = ''
running = True
while running:

    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0] and knight_rect.collidepoint(pygame.mouse.get_pos()):
        which_character = 'knight'
        running = False
    if pygame.mouse.get_pressed()[0] and wizard_rect.collidepoint(pygame.mouse.get_pos()):
        which_character = 'wizard'
        running = False
    if pygame.mouse.get_pressed()[0] and rogue_rect.collidepoint(pygame.mouse.get_pos()):
        which_character = 'rogue'
        running = False

    if knight_rect.collidepoint(pygame.mouse.get_pos()):
        window.blit(select_frame, (175, 75))

    elif wizard_rect.collidepoint(pygame.mouse.get_pos()):
        window.blit(select_frame, (50, 75))

    elif rogue_rect.collidepoint(pygame.mouse.get_pos()):
        window.blit(select_frame, (300, 75))

    display_characters()
    show_text()
    pygame.display.update()
