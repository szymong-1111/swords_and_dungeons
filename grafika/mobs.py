from player import Player
import arsenal
import potions
import random


def new_mob(mob):
    mob.equipment = [random.choice(basic_mob_loot)]
    print(mob.equipment)
    for item in mob.equipment:
        if type(item) is potions.Potion:
            mob.equipment[mob.equipment.index(item)] = potions.new_potion(item)
        elif type(item) is arsenal.Melee:
            mob.equipment[mob.equipment.index(item)] = arsenal.new_melee(item)
        elif type(item) is arsenal.Spell:
            mob.equipment[mob.equipment.index(item)] = arsenal.new_spell(item)
        elif type(item) is arsenal.Bomb:
            mob.equipment[mob.equipment.index(item)] = arsenal.new_bomb(item)

    print(mob.equipment)

    return Player(mob.img_name, mob.x, mob.y, mob.maxHp, mob.maxMana, mob.equipment,
                  equipped_weapon=mob.equipped_weapon, speed=mob.speed)


basic_mob_loot = [potions.healing_potion, potions.mana_potion]

ant_warrior = Player('ant_warrior.png', 0, 0, 50, 0, [],
                     equipped_weapon=arsenal.mandibles, speed=5)

dungeon_rat = Player('rat.png', 0, 0, 50, 0, [],
                     equipped_weapon=arsenal.fangs, speed=2)

erring_soul = Player('ghost.png', 0, 0, 75, 0, [],
                     equipped_weapon=arsenal.dagger, speed=2)



