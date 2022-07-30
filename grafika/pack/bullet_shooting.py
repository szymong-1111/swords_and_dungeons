import pygame
import math
import arsenal
from pygame import mixer

pygame.init()


def shoot_bullet_at_certain_angle(bullet, screen):
    for projectile in bullet.bullets:
        if not projectile.bulletFire:
            projectile.x = projectile.owner.x
            projectile.y = projectile.owner.y
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - projectile.x
            dy = mouse_y - projectile.y
            angle = math.atan2(dx, dy)
            projectile.xChange = (math.sin(angle) * 10) - 1
            projectile.yChange = (math.cos(angle) * 10) - 1

            projectile.fire_bullet(screen)

            break

        if bullet.mother:
            bullet.owner.equipped_weapon.bullets.append(
                arsenal.Spell(bullet.img_name, bullet.owner, bullet.dmg,
                              bullet.cost, bullet.name, explosive=bullet.explosive))


def shoot_bomb(bomb, screen):
    if not bomb.fire:
        bomb.x = bomb.owner.x
        bomb.y = bomb.owner.y
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - bomb.x
        dy = mouse_y - bomb.y
        angle = math.atan2(dx, dy)
        bomb.xChange = (math.sin(angle) * 10) - 1
        bomb.yChange = (math.cos(angle) * 10) - 1

        bomb.throw(screen)


'''        if bullet.owner.mana >= bullet.cost:

            cast_sound = mixer.Sound('fireball_cast.wav')
            cast_sound.play()
            bullet.bulletFire = True

            if not bullet.bulletFire:
                bullet.x = bullet.owner.x
                bullet.y = bullet.owner.y
                # bullet.direction()
                bullet.display_bullet(screen)
                bullet.owner.mana -= bullet.cost

        bullet.display_bullet(screen)'''

'''running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    primitive_bullet.update(x, y, 20, 20)
    pygame.draw.rect(screen, (0, 255, 0), primitive_bullet)

    x += move_x
    y += move_y

    pygame.display.update()'''
