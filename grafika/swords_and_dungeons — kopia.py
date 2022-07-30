import pygame
import random
import character_menu
import algorithm
import arsenal
import AI
import mobs
import bullet_shooting
import chests
import math
import explosions
import potions
from print_on_screen import print_on_screen
from pygame import mixer
from pygame.locals import *
from player import Player

flags = FULLSCREEN | DOUBLEBUF

# INITIALIZING PYGAME
pygame.init()

# MAKING SCREEN
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((1920, 1080), flags, 16)

# BACKGROUND
background = pygame.image.load('bg.png').convert()
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

# DEPTH METER
depth_meter = 0


# ROTATING FUNCTION
def blit_rotate_center(image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    return screen.blit(rotated_image, new_rect)


# DEALING DMG
def deal_dmg(npc, weapon):
    npc.hp -= random.randint(weapon.min_dmg, weapon.max_dmg)


# DISTANCE BETWEEN TWO OBJECTS
def collision(object1, object2):
    global hitbox_list
    global explosion_list
    global saved_count_deal_dmg
    global counter

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
            if object1.is_player:
                '''object1.xChange *= -1
                object1.yChange *= -1
                object1.move()
                object1.xChange = 0
                object1.yChange = 0'''
                if type(object2) is Player:
                    if object2.rect.left+48 >= object1.rect.right >= object2.rect.left-48:
                        if object1.xChange > 0:
                            object1.xChange = 0
                    if object2.rect.right+48 >= object1.rect.left >= object2.rect.right-48:
                        if object1.xChange < 0:
                            object1.xChange = 0
                    if object2.rect.top + 60 >= object1.rect.bottom >= object2.rect.top - 60:
                        if object1.yChange > 0:
                            object1.yChange = 0
                    if object2.rect.bottom + 60 >= object1.rect.top >= object2.rect.bottom - 60:
                        if object1.yChange < 0:
                            object1.yChange = 0
                else:
                    object1.xChange *= -1
                    object1.yChange *= -1
                    object1.move(screen)
                    object1.xChange = 0
                    object1.yChange = 0
            else:
                if object1.last_target:
                    object1.target = object1.last_target
                else:
                    object1.target = AI.find_path(object1, algorithm.paths)

            if type(object2) is Player:
                # object2.xChange *= -1
                # object2.yChange *= -1
                # object2.move()
                # object2.xChange = 0
                # object2.yChange = 0
                if object1.is_player:
                    '''object2.xChange *= -1
                    object2.yChange *= -1
                    object2.move()'''
                    object2.tracking_player = True
                    object2.xChange = 0
                    object2.yChange = 0
                    if counter - 20 > saved_count_deal_dmg:
                        hit_sound = mixer.Sound('hit.wav')
                        hit_sound.play()
                        if object2.equipped_weapon:
                            deal_dmg(object1, object2.equipped_weapon)
                            saved_count_deal_dmg = counter
                        else:
                            object1.hp -= random.randint(2, 8)
                            saved_count_deal_dmg = counter
                else:
                    if object2.last_target:
                        object2.target = object2.last_target
                    else:
                        object2.target = AI.find_path(object2, algorithm.paths)


# RANDOM X AND Y
def random_x():
    return random.randint(0, 1535)


def random_y():
    return random.randint(-1735, 535)


def frame_display():
    img = pygame.image.load('frame.png').convert_alpha()
    screen.blit(img, (0, screen_height-64))


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

print('dupa')


# PLAYER
eq_img = pygame.image.load('eq_demo1.png')
#player = Player(character_menu.which_character + '.png', 0, 300, 75, 50, [], is_player=True)
player = Player('knight.png', 0, 300, 75, 50, [], is_player=True)

if character_menu.which_character == 'knight':
    player.equipment.append(arsenal.new_melee(arsenal.warhammer))
    for _ in range(15):
        player.equipment.append(arsenal.new_melee(arsenal.small_sword))
    player.maxHp = 75

elif character_menu.which_character == 'wizard':
    player.equipment.append(arsenal.new_spell(arsenal.fireball))
    player.equipment.append(arsenal.new_spell(arsenal.flames))
    player.equipment.append(arsenal.new_spell(arsenal.fire_rumble))
    player.equipment.append(potions.new_potion(potions.healing_potion))
    player.equipment.append(potions.new_potion(potions.mana_potion))
    for _ in range(1):
        player.equipment.append(arsenal.new_bomb(arsenal.basic_bomb))
    player.maxHp = 25

elif character_menu.which_character == 'rogue':
    player.equipment.append(arsenal.new_melee(arsenal.dagger))
    player.maxHp = 50

player.hp = player.maxHp

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
    global depth_meter

    algorithm.walls.clear()
    algorithm.everything.clear()
    algorithm.spawnpoints.clear()
    algorithm.paths.clear()
    chest_list.clear()
    arsenal.free_laying_items.clear()

    player.x = 8
    player.y = 308

    if True:

        # ENEMY
        # elPrimo = Player('ant_warrior.png', 200, 316, 50, 0, [arsenal.new_melee(arsenal.warhammer)], speed=5, equipped_weapon=arsenal.new_melee(arsenal.mandibles))
        elPrimo = mobs.new_mob(mobs.ant_warrior)
        ghost = Player('the_zhodor_ant.png', random_x(), random_y(), 50, 0, [arsenal.new_melee(arsenal.warhammer)], speed=2, equipped_weapon=arsenal.new_melee(arsenal.small_sword))
        #rat_boss = Player('greater_rat_boss.png', 200, 300, 100, 0, [], speed=1)

        npcs = [
            Player(random.choice(('rat.png', 'rogue.png')), random_x(), random_y(), 50, 0, [arsenal.new_melee(arsenal.warhammer)], speed=2)
            for _ in range(5)
        ]

        npcs.append(ghost)
        npcs.append(elPrimo)
        #npcs.append(rat_boss)

        for npc in npcs:
            algorithm.everything.append(npc)

        algorithm.build_walls(screen)
        # algorithm.generate_dungeon(screen)
        algorithm.new_dungeon_generator(screen)

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

        print(algorithm.spawnpoints)
        print(list(set(algorithm.spawnpoints)))
        algorithm.spawnpoints = list(set(algorithm.spawnpoints))

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
            try:
                chest_spawnpoint = random.choices(algorithm.spawnpoints)[0]
                chest_list.append(
                    chests.Chest('basic_chest.png', chest_spawnpoint[0], chest_spawnpoint[1], chests.basic_chest_loot))
                algorithm.spawnpoints.remove(chest_spawnpoint)
            except IndexError:
                pass

        bg_y = -540
        bg_x = 0

    else:
        npcs.clear()

        algorithm.build_walls(screen)
        algorithm.make_arena()

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

        bg_y = -480
        bg_x = 0

    depth_meter += 1


new_dungeon()

dungeon_xChange = 0
dungeon_yChange = 0

# GAME LOOP
counter = 0
saved_count = 0
saved_count_eq = 0
saved_count_deal_dmg = 0

running = True
move_keys_clicked = False
w_pressing = False
s_pressing = False
a_pressing = False
d_pressing = False

while running:
    # TICKING CLOCK
    clock.tick(30)

    screen.fill((0, 0, 0))
    #screen.blit(background, (bg_x, bg_y))

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
            if math.sqrt(((thing[1]+40) - (player.x+32))**2 + ((thing[2]+40) - (player.y+32))**2) < 400:
                screen.blit(thing[0], (thing[1], thing[2]))
                thing[3] = True
            elif thing[3]:
                screen.blit(thing[4], (thing[1], thing[2]))

    for item in arsenal.free_laying_items:
        item.display(screen)
        item.is_selected(screen, player)

    for path in algorithm.paths:
        pass
        #pygame.draw.line(screen, (255, 0, 0), path[0], path[1])

    screen.blit(downstairs_img, (downstairs_x, downstairs_y))
    if go_down():
        new_dungeon()

    #pygame.draw.circle(screen, (150, 150, 150), (player.x + 32, player.y + 32), 100)

    # CHECKING FOR EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MOVEMENT BY KEYBOARD

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                a_pressing = True
                step.stop()
                step.play()
                player.xChange = -player.speed
                player.playerDirection = 'left'
            if event.key == pygame.K_d:
                d_pressing = True
                step.stop()
                step.play()
                player.xChange = player.speed
                player.playerDirection = 'right'
            if event.key == pygame.K_w:
                w_pressing = True
                step.stop()
                step.play()
                player.yChange = -player.speed
                player.playerDirection = 'up'
            if event.key == pygame.K_s:
                s_pressing = True
                step.stop()
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

            if event.key == pygame.K_x:
                pygame.draw.circle(screen, (150, 150, 0), (player.x + 32, player.y + 32), 700)

        if event.type == pygame.KEYUP:
            bg_yChange = 0
            step.stop()
            if event.key == pygame.K_w:
                w_pressing = False
            elif event.key == pygame.K_s:
                s_pressing = False
            elif event.key == pygame.K_a:
                a_pressing = False
            elif event.key == pygame.K_d:
                d_pressing = False

            if event.key == pygame.K_w:
                if player.yChange < 0:
                    player.yChange = 0
            if event.key == pygame.K_s:
                if player.yChange > 0:
                    player.yChange = 0
            if event.key == pygame.K_a:
                if player.xChange < 0:
                    player.xChange = 0
            if event.key == pygame.K_d:
                if player.xChange > 0:
                    player.xChange = 0

            if event.key == pygame.K_p or pygame.K_l:
                dungeon_yChange = 0
            if event.key == pygame.K_k or pygame.K_SEMICOLON:
                dungeon_xChange = 0

    if type(player.equipped_weapon) is arsenal.Melee:
        time_between_attack = player.equipped_weapon.time_of_slash+2
    elif type(player.equipped_weapon) is arsenal.Spell:
        time_between_attack = player.equipped_weapon.cast_speed
    else:
        time_between_attack = 10

    if counter - time_between_attack > saved_count:
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
                        '''if mouse_y > player.y and mouse_y - player.y > mouse_x - player.x:
                            player.playerDirection = 'down'''
                        if mouse_y < player.y and player.y - mouse_y > mouse_x - player.x:
                            player.playerDirection = 'up'
                    else:
                        '''if mouse_y > player.y and mouse_y - player.y > player.x - mouse_x:
                            player.playerDirection = 'down'''
                        if mouse_y < player.y and player.y - mouse_y > player.x - mouse_x:
                            player.playerDirection = 'up'

                    player.equipped_weapon.slash()

                if type(player.equipped_weapon) is arsenal.Bomb:
                    bullet_shooting.shoot_bomb(player.equipped_weapon, screen)

                if type(player.equipped_weapon) is potions.Potion:
                    player.equipped_weapon.use()

    '''if explosion_counter <= 1:
        for hitbox in hitbox_list:
            for npc in npcs:
                if pygame.Rect.colliderect(npc.rect, hitbox):
                    npc.hp -= 10
            if pygame.Rect.colliderect(player.rect, hitbox):
                player.hp -= 10'''

    explosion_counter = explosions.explode(explosion_counter, screen, npcs, player)

    for chest in chest_list:
        if math.sqrt(((chest.x + 32) - (player.x + 32)) ** 2 + ((chest.y + 32) - (player.y + 32)) ** 2) < 400:
            chest.display(screen)

    for npc in npcs:
        if math.sqrt(((npc.x + 32) - (player.x + 32)) ** 2 + ((npc.y + 32) - (player.y + 32)) ** 2) < 400:
            npc.display(screen, counter)
        npc.move(screen)
        npc.walk_around(player)
        npc.is_selected(screen)
        collision(player, npc)
        '''for npc1 in npcs:
            if not npc1 == npc:
                collision(npc, npc1)'''
        for weapon in player.equipment:
            if type(weapon) is arsenal.Spell or type(weapon) is arsenal.Bomb or type(weapon) is arsenal.Melee:
                if type(weapon) is arsenal.Spell:
                    for bullet in weapon.bullets:
                        collision(bullet, npc)
                collision(weapon, npc)

        if npc.hp == -1:
            npcs.remove(npc)

    # DISPLAYING PLAYER

    # MOVING THE CAMERA
    if offcenter_horizontal:
        if player.x > 888:
            player.x -= player.speed
            move_dungeon('x', -player.speed)
            bg_x -= player.speed
        elif player.x < 888:
            player.x += player.speed
            move_dungeon('x', player.speed)
            bg_x += player.speed

    if offcenter_vertical:
        if player.y > 518:
            player.y -= player.speed
            move_dungeon('y', -player.speed)
            bg_y -= player.speed
        elif player.y < 518:
            player.y += player.speed
            move_dungeon('y', player.speed)
            bg_y += player.speed

    if player.x > 1306:
        offcenter_horizontal = True

    if player.x < 614:
        offcenter_horizontal = True

    if player.y > 850:
        offcenter_vertical = True

    if player.y < 230:
        offcenter_vertical = True

    if player.x == 888:
        offcenter_horizontal = False
    if player.y == 518:
        offcenter_vertical = False

    # MOVING THE PLAYER AND HIS WEAPONS

    player.move(screen)
    player.display(screen, counter)

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
    player.is_selected(screen)

    # CHESTS
    for chest in chest_list:
        if not chest.exhausted:
            chest.open(player, screen)
        else:
            chest_list.remove(chest)
        chest.is_selected(screen)
        if chest.show_loot:
            if not chest.saved_count:
                chest.saved_count = counter
            if counter == chest.saved_count:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y))
            elif counter == chest.saved_count+2:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 20))
            elif counter == chest.saved_count+3:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 40))
            elif counter == chest.saved_count+4:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 60))
            elif counter == chest.saved_count+5 or counter == chest.saved_count+6:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 80))
            elif counter == chest.saved_count+7:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 60))
            elif counter == chest.saved_count+8:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 40))
            elif counter == chest.saved_count+9:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y - 20))
            elif counter == chest.saved_count+10:
                screen.blit(chest.loot.img, (chest.x + (64-chest.loot.img.get_width())/2, chest.y))
                chest.exhausted = True
                chest.show_loot = False

                chest.loot.x = chest.x+(64-chest.loot.img.get_width())/2
                chest.loot.y = chest.y
                arsenal.free_laying_items.append(chest.loot)

    # GO DOWN INFO
    if pygame.Rect(downstairs_x, downstairs_y, 80, 80).collidepoint(pygame.mouse.get_pos()):
        go_down_info = pygame.image.load('go_down_info.png').convert()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(go_down_info, (mouse_x, mouse_y))

    # PLAYER EQUIPMENT
    if player.show_eq:
        screen.blit(eq_img, (screen_width - 320, 0))
        item_x = (screen_width - 320) + 24
        item_y = 0 + 64
        loop_counter = 0
        for item in player.equipment:
            if type(item) is arsenal.Spell:
                scroll_img = pygame.image.load('scroll_demo.png')
                screen.blit(scroll_img, (item_x-16, item_y-16))
                screen.blit(item.img, (item_x, item_y))
            elif type(item) is potions.Potion:
                screen.blit(item.img, (item_x-16, item_y-16))
            elif type(item) is arsenal.Melee:
                screen.blit(item.img, (item_x, item_y-8))
            else:
                screen.blit(item.img, (item_x, item_y))
            loop_counter += 1
            if loop_counter == 4:
                loop_counter = 0
                item_x = (screen_width - 320) + 24
                item_y += 80
            else:
                item_x += 80

        slot_list = list()
        slot_loop_counter = 0
        slot_x = screen_width - 320
        slot_y = 0 + 40
        for _ in range(16):
            slot_list.append(pygame.Rect(slot_x, slot_y, 80, 80))
            slot_loop_counter += 1
            if slot_loop_counter == 4:
                slot_x = screen_width - 320
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
                        screen.blit(stats_info, (mouse_x-160, mouse_y))

                        print_on_screen('name: ' + str(item.name), screen, mouse_x - 152, mouse_y + 60)
                        if type(item) is not arsenal.Bomb and type(item) is not potions.Potion:
                            print_on_screen('min dmg: ' + str(item.min_dmg), screen, mouse_x - 152, mouse_y + 80)
                            print_on_screen('max dmg: ' + str(item.max_dmg), screen, mouse_x - 152, mouse_y + 100)
                        if type(item) is arsenal.Spell:
                            print_on_screen('cost: ' + str(item.cost), screen, mouse_x - 152, mouse_y + 120)

                if counter - 2 > saved_count_eq:
                    saved_count_eq = counter
                    if pygame.mouse.get_pressed()[0]:
                        for item in player.equipment:
                            if slot_list.index(slot) == player.equipment.index(item):
                                if type(item) is arsenal.Spell or type(item) is arsenal.Bomb or type(item) is arsenal.Melee:
                                    player.equip(item)
                                else:
                                    item.use()
                    elif pygame.mouse.get_pressed()[2]:
                        for item in player.equipment:
                            if slot_list.index(slot) == player.equipment.index(item):
                                if type(item) is arsenal.Spell:
                                    item.y = player.y
                                    if player.playerDirection == 'left':
                                        item.x = player.x
                                    else:
                                        item.x = player.x
                                    player.equipment.remove(item)
                                    try:
                                        algorithm.everything.remove(item)
                                    except ValueError:
                                        pass
                                    arsenal.free_laying_items.append(item)
                                    if item == player.equipped_weapon:
                                        player.equipped_weapon = None
                                    item.owner = None
                                else:
                                    item.y = player.y
                                    if player.playerDirection == 'left':
                                        item.x = player.x
                                    else:
                                        item.x = player.x
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
            screen.blit(scroll_img, (0, screen_height-64))
            screen.blit(player.equipped_weapon.img, (16, screen_height-48))
        elif type(player.equipped_weapon) is arsenal.Melee:
            screen.blit(player.equipped_weapon.img, (16, screen_height-55))
        elif type(player.equipped_weapon) is arsenal.Bomb:
            screen.blit(player.equipped_weapon.img, (16, screen_height-48))
        elif type(player.equipped_weapon) is potions.Potion:
            screen.blit(player.equipped_weapon.img, (0, screen_height-64))
    except AttributeError:
        pass

    # DISPLAYING DEPTH
    print_on_screen(str(depth_meter), screen, 16, 16, font_size=32)

    # UPDATING DISPLAY AND COUNTING COUNTER
    pygame.display.update()

    if counter > 1000:
        counter = 0
        saved_count = 0
        saved_count_eq = 0
        saved_count_deal_dmg = 0

    counter += 1

