import pygame
import arsenal
from pygame import mixer
import math
import algorithm
import AI



pygame.init()


def blit_rotate_center(image, topleft, angle, screen):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    return screen.blit(rotated_image, new_rect)


class Player:
    def __init__(self, img, x, y, maxHp, maxMana, equipment, equipped_weapon=None, speed=10, is_player=False):
        self.maxHp = maxHp
        self.hp = maxHp
        self.maxMana = maxMana
        self.mana = maxMana
        self.img = pygame.image.load(img).convert_alpha()
        self.img_name = img
        self.x = x
        self.y = y
        self.manarect = pygame.Rect(self.x, self.y - 25, self.mana, 10)
        self.hprect = pygame.Rect(self.x, self.y - 15, self.hp, 10)
        self.max_manarect = pygame.Rect(self.x, self.y - 25, self.maxMana, 10)
        self.max_hprect = pygame.Rect(self.x, self.y - 15, self.maxHp, 10)
        self.rect = self.img.get_rect()
        self.playerDirection = 'right'
        self.xChange = 0
        self.yChange = 0
        self.speed = speed
        self.equipped_weapon = equipped_weapon
        self.is_player = is_player
        self.equipment = equipment
        self.target = None
        self.last_target = None
        self.show_eq = False
        self.turns_of_move = 0
        self.tracking_player = False

    def display(self, screen, counter):

        for weapon in self.equipment:
            weapon.owner = self

        pygame.draw.rect(screen, (0, 0, 0), self.max_manarect)
        pygame.draw.rect(screen, (0, 0, 0), self.max_hprect)
        pygame.draw.rect(screen, (155, 0, 0), self.hprect)
        pygame.draw.rect(screen, (0, 0, 155), self.manarect)
        #pygame.draw.rect(screen, (155, 0, 0), self.rect)

        if self.is_player:
            if self.xChange or self.yChange:
                if (counter-6) % 12 == 0:
                    self.img = pygame.image.load('wizard_r.png')
                elif counter % 12 == 0:
                    self.img = pygame.image.load('wizard_l.png')
            else:
                self.img = pygame.image.load('wizard.png')

        self.max_manarect.update(self.x, self.y - 25, self.maxMana, 10)
        self.max_hprect.update(self.x, self.y - 15, self.maxHp, 10)
        self.manarect.update(self.x, self.y - 25, self.mana, 10)
        self.hprect.update(self.x, self.y - 15, self.hp, 10)
        self.rect.update(self.x + 2, self.y + 2, 60, 60)

        if self.hp > 0:
            if self.is_player:
                if self.playerDirection == 'left':
                    screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y))
                else:
                    screen.blit(self.img, (self.x, self.y))
            else:
                screen.blit(self.img, (self.x, self.y))
        else:
            if self.is_player:
                global running
                running = False
            else:
                patafian = mixer.Sound('patafian.wav')
                patafian.play()

                self.equipment[0].x = self.x
                self.equipment[0].y = self.y
                self.equipment[0].owner = None
                arsenal.free_laying_items.append(self.equipment[0])

                self.hp = -1

        # THE DIRECTION ARROW
        if self.is_player:
            direction_arrow = pygame.image.load('direction_arrow.png').convert_alpha()
            if self.playerDirection == 'right':
                blit_rotate_center(direction_arrow, (self.x + 72, self.y + 32), 270, screen)
            if self.playerDirection == 'up':
                screen.blit(direction_arrow, (self.x + 24, self.y - 40))
            if self.playerDirection == 'left':
                blit_rotate_center(direction_arrow, (self.x - 24, self.y + 32), 90, screen)
            if self.playerDirection == 'down':
                blit_rotate_center(direction_arrow, (self.x + 24, self.y + 64), 180, screen)

    def move(self, screen):
        if self.xChange or self.yChange:
            self.x += self.xChange
            self.y += self.yChange

            # RECT UPDATE
            self.max_manarect.update(self.x, self.y - 25, self.maxMana, 10)
            self.max_hprect.update(self.x, self.y - 15, self.maxHp, 10)
            self.manarect.update(self.x, self.y - 25, self.mana, 10)
            self.hprect.update(self.x, self.y - 15, self.hp, 10)
            self.rect.update(self.x+2, self.y+2, 60, 60)

            # THE DIRECTION ARROW
            if self.is_player:
                direction_arrow = pygame.image.load('direction_arrow.png').convert_alpha()
                if self.playerDirection == 'right':
                    blit_rotate_center(direction_arrow, (self.x + 72, self.y + 32), 270, screen)
                if self.playerDirection == 'up':
                    screen.blit(direction_arrow, (self.x + 24, self.y - 40))
                if self.playerDirection == 'left':
                    blit_rotate_center(direction_arrow, (self.x - 24, self.y + 32), 90, screen)
                if self.playerDirection == 'down':
                    blit_rotate_center(direction_arrow, (self.x + 24, self.y + 64), 180, screen)

    def regenerate_mana(self):

        """
        regenerates mana if it is under maximum amount (maxMana)
        :return:
        """

        if not self.mana == self.maxMana:
            if self.mana + 0.2 <= self.maxMana:
                self.mana += 0.2
            else:
                self.mana += self.maxMana - self.mana

    def equip(self, weapon):
        self.equipped_weapon = weapon

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def walk_around(self, player):
        """
        activates AI
        """
        distance_between_self_and_player = math.sqrt(((self.x+32) - (player.x+32))**2 + ((self.y+32) - (player.y+32))**2)

        if distance_between_self_and_player < 80:
            self.tracking_player = True
            '''
            dx = player.x - self.x
            dy = player.y - self.y
            angle = math.atan2(dx, dy)
            self.xChange = (math.sin(angle)) - 1
            self.yChange = (math.cos(angle)) - 1'''
            #self.last_target = self.target

            self.target = (player.x+32, player.y+32)
            if self.target[0] - 32 > self.x:
                self.yChange = 0
                self.xChange = self.speed
            elif self.target[0] - 32 < self.x:
                self.yChange = 0
                self.xChange = -self.speed
            elif self.target[1] - 40 > self.y:
                self.xChange = 0
                self.yChange = self.speed
            elif self.target[1] - 40 < self.y:
                self.xChange = 0
                self.yChange = -self.speed
        else:
            if self.tracking_player:
                self.target = AI.find_path(self, algorithm.paths)
                if self.target:
                    if self.target[0] - 32 > self.x:
                        self.yChange = 0
                        self.xChange = self.speed
                    elif self.target[0] - 32 < self.x:
                        self.yChange = 0
                        self.xChange = -self.speed
                    elif self.target[1] - 40 > self.y:
                        self.xChange = 0
                        self.yChange = self.speed
                    elif self.target[1] - 40 < self.y:
                        self.xChange = 0
                        self.yChange = -self.speed

        if self.xChange == 0 and self.yChange == 0:
            self.tracking_player = False
            if distance_between_self_and_player < 700:
                self.target = AI.seek_and_destroy(self, algorithm.paths, player)
                if self.target:
                    if self.target[0] - 32 > self.x:
                        self.yChange = 0
                        self.xChange = self.speed
                    elif self.target[0] - 32 < self.x:
                        self.yChange = 0
                        self.xChange = -self.speed
                    elif self.target[1] - 40 > self.y:
                        self.xChange = 0
                        self.yChange = self.speed
                    elif self.target[1] - 40 < self.y:
                        self.xChange = 0
                        self.yChange = -self.speed

        if self.xChange == 0 and self.yChange == 0:
            self.target = AI.follow_path(self, algorithm.paths)
            if self.target:
                if self.target[0] - 32 > self.x:
                    self.yChange = 0
                    self.xChange = self.speed
                elif self.target[0] - 32 < self.x:
                    self.yChange = 0
                    self.xChange = -self.speed
                elif self.target[1] - 40 > self.y:
                    self.xChange = 0
                    self.yChange = self.speed
                elif self.target[1] - 40 < self.y:
                    self.xChange = 0
                    self.yChange = -self.speed
        else:
            if self.target:
                if self.target == self.last_target:
                    if self.target[0] - 32 > self.x:
                        self.yChange = 0
                        self.xChange = self.speed
                    elif self.target[0] - 32 < self.x:
                        self.yChange = 0
                        self.xChange = -self.speed
                    elif self.target[1] - 40 > self.y:
                        self.xChange = 0
                        self.yChange = self.speed
                    elif self.target[1] - 40 < self.y:
                        self.xChange = 0
                        self.yChange = -self.speed
            else:
                self.xChange = 0
                self.yChange = 0

            if [self.x + 32, self.y + 40] == self.target:
                self.xChange = 0
                self.yChange = 0
                self.last_target = self.target

    def is_selected(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            select_frame = pygame.image.load('select_frame2.png')
            screen.blit(select_frame, (self.x, self.y))
