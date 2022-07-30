import pygame
import random
import math
import arsenal
import potions

pygame.init()


class Chest:
    def __init__(self, img, x, y, possible_loot):
        self.img = pygame.image.load(img).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.img.get_rect()
        self.show_loot = False
        self.loot = None
        self.possible_loot = possible_loot
        self.exhausted = False
        self.saved_count = 0

    def display(self, screen):
        self.rect.update(self.x, self.y, 64, 64)
        screen.blit(self.img, (self.x, self.y))

    def is_selected(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            select_frame = pygame.image.load('select_frame2.png').convert_alpha()
            chest_info = pygame.image.load('chest_info.png').convert()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            screen.blit(select_frame, (self.x, self.y))
            screen.blit(chest_info, (mouse_x, mouse_y))

    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

    def open(self, player, screen):
        d = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

        if not self.show_loot:
            if self.is_clicked() and d < 96:
                self.img = pygame.image.load('open_chest.png').convert_alpha()
                self.loot = random.choice(self.possible_loot)
                self.show_loot = True

        if self.show_loot:

            if type(self.loot) is arsenal.Melee:
                self.loot = arsenal.Melee(self.loot.img_name, self.loot.owner, self.loot.dmg, self.loot.name)

            elif type(self.loot) is arsenal.Bomb:
                self.loot = arsenal.new_bomb(self.loot)

            elif type(self.loot) is potions.Potion:
                self.loot = potions.new_potion(self.loot)


basic_chest_loot = [arsenal.dagger, arsenal.small_sword, arsenal.basic_bomb, potions.mana_potion, potions.healing_potion]
basic_chest = Chest('chest_demo2.png', None, None, basic_chest_loot)











