import pygame
import random
import character_menu
import algorithm
import arsenal
import AI
import bullet_shooting
import chests
import math
import explosions
from print_on_screen import print_on_screen
from pygame import mixer

# INITIALIZING PYGAME
pygame.init()

# MAKING SCREEN
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load('very_big_grey_bg.png').convert()
'''mixer.music.load('background.wav.wav')
mixer.music.play(-1)'''
step = mixer.Sound('steps.wav')

# TITLE AND ICON
pygame.display.set_caption('Swords and Dungeons')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# EXPLOSION DISPLAY
hitbox_list = list()
explosion_list = list()
explosion_counter = 0

# CLOCK
clock = pygame.time.Clock()

# CHECKING IF THE PLAYER IS OFFCENTER
offcenter_horizontal = False
offcenter_vertical = False


# ROTATING FUNCTION
def blit_rotate_center(image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    return screen.blit(rotated_image, new_rect)


# DEALING DMG
def deal_dmg(npc, weapon):
    npc.hp -= weapon.dmg


# DISTANCE BETWEEN TWO OBJECTS
def collision(object1, object2):
    global hitbox_list
    global explosion_list

    if type(object2) is Player:
        rect2 = object2.rect
    else:
        rect2 = object2
    if pygame.Rect.colliderect(object1.rect, rect2):

        if type(object1) is arsenal.Spell:
            if object1.bulletFire:

                fireball_explosion = mixer.Sound('fireball_explosion.wav')
                fireball_explosion.play()

                object1.xChange = 0
                object1.yChange = 0
                if object1.explosive:
                    explosions.explosion(object1.x, object1.y)

                object1.x = object1.owner.x
                object1.y = object1.owner.y
                object1.bulletFire = False
                arsenal.bullets_optimize(object1.bullets)

                if type(object2) is Player:
                    deal_dmg(object2, object1)

        elif type(object1) is arsenal.Bomb:
            if object1.fire:
                object1.xChange = 0
                object1.yChange = 0
                explosions.explosion(object1.x, object1.y)
                object1.x = object1.owner.x
                object1.y = object1.owner.y
                object1.fire = False
                object1.owner.equipment.remove(object1)
                if object1 == player.equipped_weapon:
                    player.equipped_weapon = None

        elif type(object1) is arsenal.Melee:
            if object1.slashing:
                hit_sound = mixer.Sound('hit.wav')
                hit_sound.play()
                deal_dmg(object2, object1)

        else:

            object1.xChange *= -1
            object1.yChange *= -1
            object1.move()
            object1.xChange = 0
            object1.yChange = 0

            if type(object2) is Player:
                # object2.xChange *= -1
                # object2.yChange *= -1
                # object2.move()
                object2.xChange = 0
                object2.yChange = 0


# RANDOM X AND Y
def random_x():
    return random.randint(0, 1535)


def random_y():
    return random.randint(-1735, 535)


def frame_display():
    img = pygame.image.load('frame.png').convert_alpha()
    screen.blit(img, (0, 536))


def move_dungeon(dimension, amount):
    global downstairs_y
    global downstairs_x

    for thing in algorithm.everything:
        if type(thing) is pygame.Rect or type(thing) is Player or type(thing) is arsenal.Spell:
            if dimension == 'x':
                thing.x += amount
            elif dimension == 'y':
                thing.y += amount
        elif type(thing) is arsenal.Spell:
            if dimension == 'x':
                thing.x += amount
            elif dimension == 'y':
                thing.y += amount
        elif type(thing) is arsenal.Bomb:
            if dimension == 'x':
                thing.x += amount
            elif dimension == 'y':
                thing.y += amount
        else:
            if dimension == 'x':
                print(thing[1])
                thing[1] += amount
            elif dimension == 'y':
                thing[2] += amount
            pass

    for item in arsenal.free_laying_items:
        if dimension == 'x':
            item.x += amount
        elif dimension == 'y':
            item.y += amount

    for wall in algorithm.walls:
        if dimension == 'x':
            wall.x += amount
        elif dimension == 'y':
            wall.y += amount

    for path in algorithm.paths:
        if dimension == 'x':
            path[0][0] += amount
            path[1][0] += amount
        elif dimension == 'y':
            path[0][1] += amount
            path[1][1] += amount

    if dimension == 'x':
        downstairs_x += amount
    elif dimension == 'y':
        downstairs_y += amount

    for chest in chest_list:
        if dimension == 'x':
            chest.x += amount
        elif dimension == 'y':
            chest.y += amount


def go_down():
    downstairs_rect = pygame.Rect(downstairs_x, downstairs_y, 80, 80)

    distance = math.sqrt((downstairs_x - player.x) ** 2 + (downstairs_y - player.y) ** 2)

    if downstairs_rect.collidepoint(pygame.mouse.get_pos()):
        select_frame = pygame.image.load('select_frame4.png').convert_alpha()

        screen.blit(select_frame, (downstairs_x, downstairs_y))

        if pygame.mouse.get_pressed()[0]:
            if distance < 96:
                return True

    return False


# CLASS TO CREATE NPCS

class Player:
    def __init__(self, img, x, y, hp, maxMana, equipment, equipped_weapon=None, speed=5, is_player=False, target=None):
        self.hp = hp
        self.maxMana = maxMana
        self.mana = maxMana
        self.img = pygame.image.load(img).convert_alpha()
        self.x = x
        self.y = y
        self.manarect = pygame.Rect(self.x, self.y - 25, self.mana, 10)
        self.hprect = pygame.Rect(self.x, self.y - 15, self.hp, 10)
        self.rect = self.img.get_rect()
        self.playerDirection = 'right'
        self.xChange = 0
        self.yChange = 0
        self.speed = speed
        self.equipped_weapon = equipped_weapon
        self.is_player = is_player
        self.equipment = equipment
        self.target = target
        self.show_eq = False

    def display(self):
        pygame.draw.rect(screen, (255, 0, 0), self.hprect)
        pygame.draw.rect(screen, (0, 0, 255), self.manarect)
        self.manarect.update(self.x, self.y - 25, self.mana, 10)
        self.hprect.update(self.x, self.y - 15, self.hp, 10)
        self.rect.update(self.x, self.y, self.img.get_width(), self.img.get_height())

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
                npcs.remove(self)

        # THE DIRECTION ARROW
        if self.is_player:
            direction_arrow = pygame.image.load('direction_arrow.png').convert_alpha()
            if player.playerDirection == 'right':
                blit_rotate_center(direction_arrow, (self.x + 72, self.y + 32), 270)
            if player.playerDirection == 'up':
                screen.blit(direction_arrow, (self.x + 24, self.y - 40))
            if player.playerDirection == 'left':
                blit_rotate_center(direction_arrow, (self.x - 24, self.y + 32), 90)
            if player.playerDirection == 'down':
                blit_rotate_center(direction_arrow, (self.x + 24, self.y + 64), 180)

    def move(self):

        for weapon in self.equipment:
            weapon.owner = self

        if self.xChange or self.yChange:
            self.x += self.xChange
            self.y += self.yChange

            # RECT UPDATE
            self.manarect.update(self.x, self.y - 25, self.mana, 10)
            self.hprect.update(self.x, self.y - 15, self.hp, 10)
            self.rect.update(self.x, self.y, self.img.get_width(), self.img.get_height())

            # BOUNDARIES
            if self.is_player:
                global bg_x
                global bg_y
                global offcenter_horizontal
                global offcenter_vertical

                if self.x > 672:
                    offcenter_horizontal = True

                if self.x < 128:
                    offcenter_horizontal = True

                if self.y > 472:
                    offcenter_vertical = True

                if self.y < 128:
                    offcenter_vertical = True

                if self.x == 400:
                    offcenter_horizontal = False
                if self.y == 300:
                    offcenter_vertical = False

            # THE DIRECTION ARROW
            if self.is_player:
                direction_arrow = pygame.image.load('direction_arrow.png').convert_alpha()
                if player.playerDirection == 'right':
                    blit_rotate_center(direction_arrow, (self.x + 72, self.y + 32), 270)
                if player.playerDirection == 'up':
                    screen.blit(direction_arrow, (self.x + 24, self.y - 40))
                if player.playerDirection == 'left':
                    blit_rotate_center(direction_arrow, (self.x - 24, self.y + 32), 90)
                if player.playerDirection == 'down':
                    blit_rotate_center(direction_arrow, (self.x + 24, self.y + 64), 180)

    def regenerate_mana(self):

        """
        regenerates mana if it is under maximum amount (maxMana)
        :return:
        """

        if not self.mana == self.maxMana:
            if self.mana + 0.1 <= self.maxMana:
                self.mana += 0.1
            else:
                self.mana += self.maxMana - self.mana

    def equip(self, weapon):
        self.equipped_weapon = weapon

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def walk_around(self):
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
            if [self.x + 32, self.y + 40] == self.target:
                self.xChange = 0
                self.yChange = 0

    def show_xy(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render('x: ' + str(self.x) + 'y: ' + str(self.y), True, (255, 255, 255))
        screen.blit(text, (20, 30))

    def is_selected(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            select_frame = pygame.image.load('select_frame2.png')
            screen.blit(select_frame, (self.x, self.y))


# PLAYER
eq_img = pygame.image.load('eq_demo1.png')
player = Player(character_menu.which_character + '.png', 0, 300, 75, 50, [], is_player=True)

if character_menu.which_character == 'knight':
    for _ in range(16):
        player.equipment.append(arsenal.new_melee(arsenal.small_sword))
    player.hp = 75

elif character_menu.which_character == 'wizard':
    player.equipment.append(arsenal.new_spell(arsenal.fireball))
    for _ in range(8):
        player.equipment.append(arsenal.new_bomb(arsenal.basic_bomb))
    player.hp = 25

elif character_menu.which_character == 'rogue':
    player.equipment.append(arsenal.new_melee(arsenal.dagger))
    player.hp = 50

npcs = list()
chest_list = list()

downstairs_x = 0
downstairs_y = 0
downstairs_img = None

bg_x = 0
bg_y = 0


def new_dungeon():
    global downstairs_y
    global downstairs_x
    global downstairs_img
    global npcs
    global chest_list
    global bg_x
    global bg_y

    algorithm.walls.clear()
    algorithm.everything.clear()
    algorithm.spawnpoints.clear()
    algorithm.paths.clear()
    chest_list.clear()
    arsenal.free_laying_items.clear()

    player.x = 0
    player.y = 300

    # ENEMY
    elPrimo = Player('knight.png', 200, 316, 50, 0, [], speed=1)
    ghost = Player('ghost.png', random_x(), random_y(), 50, 50, [], speed=1)
    rat_boss = Player('greater_rat_boss.png', 200, 300, 100, 0, [], speed=1)

    npcs = [
        Player(random.choice(('rat.png', 'rogue.png')), random_x(), random_y(), 50, 0, [], speed=1)
        for _ in range(5)
    ]

    npcs.append(ghost)
    npcs.append(elPrimo)
    npcs.append(rat_boss)

    for npc in npcs:
        algorithm.everything.append(npc)

    algorithm.build_walls(screen)
    algorithm.generate_dungeon(screen)

    to_remove = []
    for wall in algorithm.walls:
        for thing in algorithm.everything:
            if type(thing) is pygame.Rect:
                if pygame.Rect.colliderect(thing, wall):
                    to_remove.append(wall)

    for stuff in to_remove:
        try:
            algorithm.walls.remove(stuff)
        except ValueError:
            pass

    for npc in npcs:
        spawnpoint = random.choices(algorithm.spawnpoints)[0]
        npc.x = spawnpoint[0]
        npc.y = spawnpoint[1]
        algorithm.spawnpoints.remove(spawnpoint)

    downstairs = random.choices(algorithm.spawnpoints)[0]
    downstairs_x = downstairs[0] - 8
    downstairs_y = downstairs[1]
    downstairs_img = pygame.image.load('downstairs_demo.png')
    algorithm.spawnpoints.remove(downstairs)

    for _ in range(random.randint(3, 6)):
        chest_spawnpoint = random.choices(algorithm.spawnpoints)[0]
        chest_list.append(
            chests.Chest('chest_demo2.png', chest_spawnpoint[0], chest_spawnpoint[1], [arsenal.dagger,
                                                                                       arsenal.small_sword,
                                                                                       arsenal.basic_bomb]))
        algorithm.spawnpoints.remove(chest_spawnpoint)

    bg_y = -2000
    bg_x = 0


new_dungeon()

dungeon_xChange = 0
dungeon_yChange = 0

# GAME LOOP
counter = 0
saved_count = 0
show_warning = False
running = True
while running:
    # TICKING CLOCK
    clock.tick(60)

    screen.fill((0, 255, 255))
    screen.blit(background, (bg_x, bg_y))

    for wall in algorithm.walls:
        collision(player, wall)
        pygame.draw.rect(screen, (0, 0, 0), wall)

    for thing in algorithm.everything:
        if type(thing) is Player:
            pass
        elif type(thing) is pygame.Rect:
            pass
        elif type(thing) is arsenal.Spell:
            pass
        elif type(thing) is arsenal.Bomb:
            pass
        else:
            screen.blit(thing[0], (thing[1], thing[2]))

    for item in arsenal.free_laying_items:
        item.display(screen)
        item.is_selected(screen, player)

    for path in algorithm.paths:
        pygame.draw.line(screen, (255, 0, 0), path[0], path[1])

    screen.blit(downstairs_img, (downstairs_x, downstairs_y))
    if go_down():
        new_dungeon()

    # CHECKING FOR EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MOVEMENT BY KEYBOARD

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                step.play()
                player.xChange = -player.speed
                player.playerDirection = 'left'
            if event.key == pygame.K_d:
                step.play()
                player.xChange = player.speed
                player.playerDirection = 'right'
            if event.key == pygame.K_w:
                step.play()
                player.yChange = -player.speed
                player.playerDirection = 'up'
            if event.key == pygame.K_s:
                step.play()
                player.yChange = player.speed
                player.playerDirection = 'down'

            if event.key == pygame.K_UP:
                player.playerDirection = 'up'
            if event.key == pygame.K_DOWN:
                player.playerDirection = 'down'
            if event.key == pygame.K_RIGHT:
                player.playerDirection = 'right'
            if event.key == pygame.K_LEFT:
                player.playerDirection = 'left'

            if event.key == pygame.K_SPACE:
                if type(player.equipped_weapon) is arsenal.Melee:
                    player.equipped_weapon.slash()

            if event.key == pygame.K_1:
                try:
                    player.equip(player.equipment[0])
                except IndexError:
                    player.equip(None)
            if event.key == pygame.K_2:
                try:
                    player.equip(player.equipment[1])
                except IndexError:
                    player.equip(None)
            if event.key == pygame.K_3:
                try:
                    player.equip(player.equipment[2])
                except IndexError:
                    player.equip(None)
            if event.key == pygame.K_4:
                try:
                    player.equip(player.equipment[3])
                except IndexError:
                    player.equip(None)
            if event.key == pygame.K_0:
                player.equip(None)

            if event.key == pygame.K_ESCAPE:
                player.show_eq = False
                for chest in chest_list:
                    if chest.show_loot:
                        if len(player.equipment) <= 15:
                            player.equipment.append(chest.loot)
                        else:
                            loot = chest.loot
                            loot.x = chest.x
                            loot.y = chest.y
                            arsenal.free_laying_items.append(loot)
                        chest_list.remove(chest)

            if event.key == pygame.K_e:
                player.show_eq = True

        if event.type == pygame.KEYUP:
            bg_yChange = 0
            step.stop()
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player.xChange = 0
            if event.key == pygame.K_UP or pygame.K_DOWN:
                player.yChange = 0
            if event.key == pygame.K_p or pygame.K_l:
                dungeon_yChange = 0
            if event.key == pygame.K_k or pygame.K_SEMICOLON:
                dungeon_xChange = 0

    if counter - 9 > saved_count:
        if not player.show_eq:
            if pygame.mouse.get_pressed()[0]:
                saved_count = counter
                if type(player.equipped_weapon) is arsenal.Spell:
                    bullet_shooting.shoot_bullet_at_certain_angle(player.equipped_weapon, screen)

                if type(player.equipped_weapon) is arsenal.Melee:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if mouse_x > player.x:
                        player.playerDirection = 'right'
                    elif mouse_x < player.x:
                        player.playerDirection = 'left'

                    if player.playerDirection == 'right':
                        if mouse_y > player.y and mouse_y - player.y > mouse_x - player.x:
                            player.playerDirection = 'down'
                        elif mouse_y < player.y and player.y - mouse_y > mouse_x - player.x:
                            player.playerDirection = 'up'
                    else:
                        if mouse_y > player.y and mouse_y - player.y > player.x - mouse_x:
                            player.playerDirection = 'down'
                        elif mouse_y < player.y and player.y - mouse_y > player.x - mouse_x:
                            player.playerDirection = 'up'

                    player.equipped_weapon.slash()

                if type(player.equipped_weapon) is arsenal.Bomb:
                    bullet_shooting.shoot_bomb(player.equipped_weapon, screen)

    '''if explosion_counter <= 1:
        for hitbox in hitbox_list:
            for npc in npcs:
                if pygame.Rect.colliderect(npc.rect, hitbox):
                    npc.hp -= 10
            if pygame.Rect.colliderect(player.rect, hitbox):
                player.hp -= 10'''

    explosion_counter = explosions.explode(explosion_counter, screen, npcs, player)

    for chest in chest_list:
        chest.display(screen)

    for npc in npcs:
        npc.display()
        npc.move()
        npc.walk_around()
        npc.is_selected()
        collision(player, npc)
        for weapon in player.equipment:
            if type(weapon) is arsenal.Spell:
                for bullet in weapon.bullets:
                    collision(bullet, npc)
            collision(weapon, npc)

    # DISPLAYING PLAYER

    # MOVING THE CAMERA
    if offcenter_horizontal:
        if player.x > 400:
            player.x -= player.speed
            move_dungeon('x', -player.speed)
            bg_x -= player.speed
        elif player.x < 400:
            player.x += player.speed
            move_dungeon('x', player.speed)
            bg_x += player.speed

    if offcenter_vertical:
        if player.y > 300:
            player.y -= player.speed
            move_dungeon('y', -player.speed)
            bg_y -= player.speed
        elif player.y < 300:
            player.y += player.speed
            move_dungeon('y', player.speed)
            bg_y += player.speed

    # MOVING THE PLAYER AND HIS WEAPONS
    player.move()
    player.display()

    for weapon in player.equipment:
        if type(weapon) is arsenal.Melee:
            weapon.move()
            weapon.display(screen)
        elif type(weapon) is arsenal.Spell:
            for bullet in weapon.bullets:

                bullet.move(screen)

                if not bullet.bulletFire:
                    bullet.x = player.x
                    bullet.y = player.y

                if bullet.bulletFire:
                    for wall in algorithm.walls:
                        collision(bullet, wall)
        elif type(weapon) is arsenal.Bomb:
            weapon.move(screen)
            if weapon.fire:
                for wall in algorithm.walls:
                    collision(weapon, wall)

    player.regenerate_mana()
    player.is_selected()

    # CHESTS
    for chest in chest_list:
        chest.open(player, screen)
        chest.is_selected(screen)

    # GO DOWN INFO
    if pygame.Rect(downstairs_x, downstairs_y, 80, 80).collidepoint(pygame.mouse.get_pos()):
        go_down_info = pygame.image.load('go_down_info.png').convert()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(go_down_info, (mouse_x, mouse_y))

    # PLAYER EQUIPMENT
    if player.show_eq:
        screen.blit(eq_img, (400 - 160, 300 - 160))
        item_x = (400 - 160) + 24
        item_y = (300 - 160) + 64
        loop_counter = 0
        for item in player.equipment:
            if type(item) is arsenal.Spell:
                scroll_img = pygame.image.load('scroll_demo.png')
                screen.blit(scroll_img, (item_x-16, item_y-16))
            screen.blit(item.img, (item_x, item_y))
            loop_counter += 1
            if loop_counter == 4:
                loop_counter = 0
                item_x = (400 - 160) + 24
                item_y += 80
            else:
                item_x += 80

        slot_list = list()
        slot_loop_counter = 0
        slot_x = 400 - 160
        slot_y = 300 - 160 + 40
        for _ in range(16):
            slot_list.append(pygame.Rect(slot_x, slot_y, 80, 80))
            slot_loop_counter += 1
            if slot_loop_counter == 4:
                slot_x = 400 - 160
                slot_y += 80
                slot_loop_counter = 0
            else:
                slot_x += 80

        for slot in slot_list:
            if slot.collidepoint(pygame.mouse.get_pos()):
                select_frame = pygame.image.load('select_frame3.png').convert_alpha()
                screen.blit(select_frame, (slot.x, slot.y))
                for item in player.equipment:
                    if slot_list.index(slot) == player.equipment.index(item):
                        stats_info = pygame.image.load('stats_info.png').convert()
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        screen.blit(stats_info, (mouse_x, mouse_y))

                        print_on_screen('name: ' + str(item.name), screen, mouse_x + 8, mouse_y + 60)
                        if type(item) is not arsenal.Bomb:
                            print_on_screen('dmg: ' + str(item.dmg), screen, mouse_x + 8, mouse_y + 80)
                        if type(item) is arsenal.Spell:
                            print_on_screen('cost: ' + str(item.cost), screen, mouse_x + 8, mouse_y + 100)

                if pygame.mouse.get_pressed()[0]:
                    for item in player.equipment:
                        if slot_list.index(slot) == player.equipment.index(item):
                            player.equip(item)
                elif pygame.mouse.get_pressed()[2]:
                    for item in player.equipment:
                        if slot_list.index(slot) == player.equipment.index(item):
                            if type(item) is arsenal.Spell:
                                warning = pygame.image.load('perm_delet_warning.png').convert()
                                show_warning = True
                                to_remove_from_equipment = item
                            else:
                                if player.playerDirection == 'left':
                                    item.x += 20
                                else:
                                    item.x -= 20
                                player.equipment.remove(item)
                                arsenal.free_laying_items.append(item)
                                if item == player.equipped_weapon:
                                    player.equipped_weapon = None
                                item.owner = None

    # FRAME FOR EQUIPPED ITEM
    frame_display()
    try:
        if type(player.equipped_weapon) is arsenal.Spell:
            scroll_img = pygame.image.load('scroll_demo.png')
            screen.blit(scroll_img, (0, 536))
            screen.blit(player.equipped_weapon.img, (16, 552))
        elif type(player.equipped_weapon) is arsenal.Melee:
            screen.blit(player.equipped_weapon.img, (16, 545))
        elif type(player.equipped_weapon) is arsenal.Bomb:
            screen.blit(player.equipped_weapon.img, (16, 552))
    except AttributeError:
        pass

    # PERM DELETING WARNING
    if show_warning:
        player.show_eq = False
        screen.blit(warning, (320, 220))
        yes_rect = pygame.Rect(348, 417, 81, 27)
        no_rect = pygame.Rect(451, 417, 81, 27)
        if yes_rect.collidepoint(pygame.mouse.get_pos()):
            choice_select_frame = pygame.image.load('select_frame5.png').convert_alpha()
            screen.blit(choice_select_frame, (348, 417))
            if pygame.mouse.get_pressed()[0]:
                player.equipment.remove(to_remove_from_equipment)
                if to_remove_from_equipment == player.equipped_weapon:
                    player.equipped_weapon = None
                show_warning = False

        if no_rect.collidepoint(pygame.mouse.get_pos()):
            choice_select_frame = pygame.image.load('select_frame5.png').convert_alpha()
            screen.blit(choice_select_frame, (451, 417))
            if pygame.mouse.get_pressed()[0]:
                show_warning = False

    # UPDATING DISPLAY AND COUNTING COUNTER
    pygame.display.update()

    if counter > 1000:
        counter = 0
        saved_count = 0

    counter += 1
