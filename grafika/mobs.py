from player import Player
import arsenal
import potions
import random


def new_mob(mob):
    return Player(mob.img_name, mob.x, mob.y, mob.maxHp, mob.maxMana, mob.equipment,
                  equipped_weapon=mob.equipped_weapon, speed=mob.speed)


basic_mob_loot = [potions.new_potion(potions.healing_potion), potions.new_potion(potions.healing_potion)]
ant_warrior = Player('ant_warrior.png', 0, 0, 50, 0, [random.choice(basic_mob_loot)],
                     equipped_weapon=arsenal.mandibles, speed=5)



