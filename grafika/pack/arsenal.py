import math
import explosions
import pygame
from pygame import mixer
import algorithm

pygame.init()

free_laying_items = list()


def new_melee(melee):
    return Melee(melee.img_name, melee.owner, melee.dmg, melee.name)


def new_spell(spell):
    return Spell(spell.img_name, spell.owner, spell.dmg, spell.cost, spell.name, mother=True, explosive=spell.explosive)


def new_bomb(bomb):
    return Bomb(bomb.img_name, bomb.owner, bomb.name)


# ROTATING FUNCTION
def blit_rotate_center(image, topleft, angle, screen, direction):
    for _ in range(1):
        rotated_image = pygame.transform.rotate(image, angle)
        if direction == 'left':
            x = image.get_rect(topleft=topleft).center[0]-16
        elif direction == 'right':
            x = image.get_rect(topleft=topleft).center[0]+16
        else:
            x = image.get_rect(topleft=topleft).center[0]
        y = image.get_rect(topleft=topleft).center[1]+16
        new_rect = rotated_image.get_rect(center=(x, y))

        if direction == 'up':
            screen.blit(pygame.transform.flip(rotated_image, True, False), new_rect)
        else:
            screen.blit(rotated_image, new_rect)

        return rotated_image


# OPTIMIZATION FUNCTION FOR BULLETS
def bullets_optimize(bullets):
    for bullet in bullets:
        if not bullet.bulletFire:
            if bullet.mother:
                pass
            else:
                bullets.remove(bullet)


class Spell:
    def __init__(self, img, owner, dmg, cost, name, bulletFire=False, speed=10, mother=False, explosive=False):
        self.cost = cost
        self.dmg = dmg
        self.img_name = img
        self.img = pygame.image.load(img).convert_alpha()
        self.owner = owner
        self.name = name

        self.x = 0
        self.y = 0
        self.savedDirection = 'right'

        self.bulletFire = bulletFire
        self.rect = self.img.get_rect()
        self.xChange = 0
        self.yChange = 0
        self.speed = speed
        self.mother = mother
        self.bullets = [self]
        self.scroll = pygame.image.load('scroll_demo.png').convert_alpha()
        self.explosive = explosive

    def display_bullet(self, screen):
        self.bulletFire = True
        screen.blit(self.img, (self.x + 16, self.y + 16))

    def move(self, screen):

        # RECT UPDATE
        self.rect.update(self.x + 16, self.y + 16, 32, 32)

        if self.x > 800:
            self.x = self.owner.x
            self.y = self.owner.y
            self.bulletFire = False
            bullets_optimize(self.bullets)
        if self.x < -32:
            self.x = self.owner.x
            self.y = self.owner.y
            self.bulletFire = False
            bullets_optimize(self.bullets)
        if self.y > 600:
            self.x = self.owner.x
            self.y = self.owner.y
            self.bulletFire = False
            bullets_optimize(self.bullets)
        if self.y < -32:
            self.x = self.owner.x
            self.y = self.owner.y
            self.bulletFire = False
            bullets_optimize(self.bullets)

        if self.bulletFire:
            self.display_bullet(screen)
            if True:     # if self.savedDirection == 'up' or self.savedDirection == 'down':
                self.y += self.yChange
            if True:     # elif self.savedDirection == 'right' or self.savedDirection == 'left':
                self.x += self.xChange

    def fire_bullet(self, screen):
        if self not in algorithm.everything:
            algorithm.everything.append(self)

        for bullet in self.bullets:
            if self.owner.mana >= self.cost:

                cast_sound = mixer.Sound('fireball_cast.wav')
                cast_sound.play()

                if not bullet.bulletFire:
                    bullet.x = bullet.owner.x
                    bullet.y = bullet.owner.y
                    bullet.display_bullet(screen)
                    bullet.owner.mana -= bullet.cost
                    break

                if self.mother:
                    self.owner.equipped_weapon.bullets.append(
                        Spell(self.img_name, self.owner, self.dmg,
                              self.cost, self.name, explosive=self.explosive))
        # THIS LOOP IS REQUIRED TO OPTIMIZE CODE SO THAT THE LOOP DOESNT KEEP TRASH IN ITSELF
        for bullet in self.bullets:
            if not bullet.bulletFire:
                if bullet.mother:
                    pass
                else:
                    self.bullets.remove(bullet)

    '''def display(self, screen):
        if not self.owner:
            self.rect.update((self.x+16, self.y+16, self.img.get_width(), self.img.get_height()))
            screen.blit(self.scroll, (self.x, self.y))
            screen.blit(self.img, (self.x+16, self.y+16))

    def is_selected(self, screen, player):
        if not self.owner:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                select_frame = pygame.image.load('select_frame2.png').convert_alpha()
                screen.blit(select_frame, (self.x, self.y))
                if pygame.mouse.get_pressed()[0]:
                    d = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
                    if d < 96:
                        player.equipment.append(self)
                        free_laying_items.remove(self)'''


class Melee:
    def __init__(self, img, owner, dmg, name):
        self.img = pygame.image.load(img).convert_alpha()
        self.img_name = img
        self.owner = owner

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

        self.real_rect = self.img.get_rect()
        self.dmg = dmg
        self.slashing_time = 0
        self.slashing = False
        self.name = name

    def slash(self):
        if not self.slashing and not self.slashing_time:
            slash_sound = mixer.Sound('slash.wav')
            slash_sound.play()
            self.slashing_time = 7
            self.slashing = True

    def move(self):
        self.real_rect.update((self.x, self.y, self.img.get_width(), self.img.get_height()))
        if self.owner.playerDirection == 'left':
            self.rect.update(self.x - 32, self.y, 64, 96)
            self.x = self.owner.x - 16
        elif self.owner.playerDirection == 'right' or self.owner.playerDirection == 'down':
            self.rect.update(self.x, self.y, 64, 96)
            self.x = self.owner.x + 50
        elif self.owner.playerDirection == 'up':
            self.rect.update(self.x - 48, self.y - 64, 64, 48)
            self.x = self.owner.x + 50
        '''elif self.owner.playerDirection == 'down':
            self.rect.update(self.x - 48, self.y + 64, 64, 64)
            self.x = self.owner.x + 50'''
        self.y = self.owner.y + 5

    def display(self, screen):
        if self.owner:
            if self.owner.equipped_weapon == self:
                # pygame.draw.rect(screen, (255, 255, 0), self.rect)
                if self.slashing_time > 0:
                    if self.owner.playerDirection == 'left':
                        if self.slashing_time < 5:
                            self.y += 32
                            blit_rotate_center(pygame.transform.flip(self.img, True, False), self.real_rect.topleft, 180, screen, 'up')

                    elif self.owner.playerDirection == 'right':
                        if self.slashing_time < 5:
                            self.y += 32
                            blit_rotate_center(self.img, self.real_rect.topleft, 180, screen, 'up')
                    elif self.owner.playerDirection == 'up':
                        self.y -= 32
                        screen.blit(self.img, (self.x, self.y))
                    '''elif self.owner.playerDirection == 'down':
                        if self.slashing_time < 5:
                            self.y += 32
                            blit_rotate_center(self.img, self.real_rect.topleft, 180, screen, 'up')'''
                    self.slashing_time -= 1
                    self.slashing = False
                else:
                    if self.owner.playerDirection == 'left':
                        screen.blit(pygame.transform.flip(self.img, True, False), (self.x, self.y-8))
                    else:
                        screen.blit(self.img, (self.x, self.y-8))
                if self.slashing_time > 4:
                    if self.owner.playerDirection == 'right':   # self.owner.playerDirection == 'down' or
                        blit_rotate_center(self.img, self.real_rect.topleft, 285, screen, 'right')
                    elif self.owner.playerDirection == 'left':
                        blit_rotate_center(pygame.transform.flip(self.img, True, False), self.real_rect.topleft, 75, screen, 'left')
        else:
            self.real_rect.update((self.x, self.y, self.img.get_width(), self.img.get_height()))
            screen.blit(self.img, (self.x, self.y))

    def is_selected(self, screen, player):
        if not self.owner:
            if self.real_rect.collidepoint(pygame.mouse.get_pos()):
                select_frame = pygame.image.load('select_frame2.png').convert_alpha()
                screen.blit(select_frame, (self.x-16, self.y-8))
                if pygame.mouse.get_pressed()[0]:
                    d = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
                    if d < 96:
                        if len(player.equipment) <= 15:
                            player.equipment.append(self)
                            free_laying_items.remove(self)


class Bomb:
    def __init__(self, img, owner, name):
        self.img = pygame.image.load(img).convert_alpha()
        self.img_name = img
        self.owner = owner
        self.name = name
        self.x = 0
        self.y = 0
        self.rect = self.img.get_rect()
        self.xChange = 0
        self.yChange = 0
        self.fire = False

    def display(self, screen):
        screen.blit(self.img, (self.x, self.y))
        self.rect.update(self.x, self.y, 32, 32)

    def throw(self, screen):
        #throw = mixer.Sound('bomb_throw.wav')
        #mixer.Sound.play(throw)
        self.fire = True
        if self not in algorithm.everything:
            algorithm.everything.append(self)

        self.x = self.owner.x+16
        self.y = self.owner.y+16

        self.display(screen)
        #self.owner.equipment.remove(self)

    def move(self, screen):
        self.rect.update(self.x, self.y, 32, 32)
        if self.fire:
            self.display(screen)
        else:
            self.x = self.owner.x+16
            self.y = self.owner.y+16

        if self.x > 800:
            explosions.explosion(self.x, self.y)
            self.owner.equipment.remove(self)
            if self.owner.equipped_weapon == self:
                self.owner.equipped_weapon = None
            algorithm.everything.remove(self)
            self.fire = False
        if self.x < -32:
            explosions.explosion(self.x, self.y)
            self.owner.equipment.remove(self)
            if self.owner.equipped_weapon == self:
                self.owner.equipped_weapon = None
            algorithm.everything.remove(self)
            self.fire = False
        if self.y > 600:
            explosions.explosion(self.x, self.y)
            self.owner.equipment.remove(self)
            if self.owner.equipped_weapon == self:
                self.owner.equipped_weapon = None
            algorithm.everything.remove(self)
            self.fire = False
        if self.y < -32:
            explosions.explosion(self.x, self.y)
            self.owner.equipment.remove(self)
            if self.owner.equipped_weapon == self:
                self.owner.equipped_weapon = None
            algorithm.everything.remove(self)
            self.fire = False

        self.x += self.xChange
        self.y += self.yChange

    def is_selected(self, screen, player):
        if not self.owner:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                select_frame = pygame.image.load('select_frame2.png').convert_alpha()
                screen.blit(select_frame, (self.x-16, self.y-16))
                if pygame.mouse.get_pressed()[0]:
                    d = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
                    if d < 96:
                        if len(player.equipment) <= 15:
                            player.equipment.append(self)
                            free_laying_items.remove(self)


# TEMPLATES
small_sword = Melee('small_sword.png', None, 10, 'small sword')
dagger = Melee('dagger.png', None, 10, 'dagger')
fireball = Spell('new_fireball.png', None, 10, 10, 'fireball', mother=True)
basic_bomb = Bomb('bomb_demo.png', None, 'basic bomb')
