import pygame
import math
import arsenal
from pygame import mixer

pygame.init()


def new_potion(potion):
    return Potion(potion.img_name, potion.effect, potion.name, potion.owner)


class Potion:
    def __init__(self, img, effect, name, owner):
        self.img = pygame.image.load(img)
        self.img_name = img
        self.effect = effect
        self.name = name
        self.owner = owner
        self.x = 0
        self.y = 0
        self.rect = self.img.get_rect()

    def use(self):

        drink_sound = mixer.Sound('drink_potion.wav')
        drink_sound.play()

        if self.effect == 0:
            if self.owner.hp+10 <= self.owner.maxHp:
                self.owner.hp += 10
            elif self.owner.hp+10 > self.owner.maxHp:
                self.owner.hp += self.owner.maxHp-self.owner.hp
        elif self.effect == 1:
            self.owner.mana = self.owner.maxMana

        self.owner.equipment.remove(self)
        if self.owner.equipped_weapon == self:
            self.owner.equipped_weapon = None

    def display(self, screen):
        self.rect.update(self.x, self.y, 64, 64)
        screen.blit(self.img, (self.x, self.y))

    def is_selected(self, screen, player):
        if not self.owner:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                select_frame = pygame.image.load('select_frame2.png').convert_alpha()
                screen.blit(select_frame, (self.x, self.y))
                if pygame.mouse.get_pressed()[0]:
                    d = math.sqrt(((self.x + 32) - (player.x + 32)) ** 2 + ((self.y + 32) - (player.y + 32)) ** 2)
                    if d < 120:
                        if len(player.equipment) <= 15:
                            player.equipment.append(self)
                            arsenal.free_laying_items.remove(self)


healing_potion = Potion('potion_demo.png', 0, 'healing potion', None)
mana_potion = Potion('blue_potion.png', 1, 'mana potion', None)
