import logging
import os

import math
import sys

from itertools import combinations, product


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="w",
)

boss_hp = 100
boss_damage = 8
boss_defence = 2

my_hp = 100

weapons = {
    "Dagger": (8, 4),
    "Shortsword": (10, 5),
    "Warhammer": (25, 6),
    "Longsword": (40, 7),
    "Greataxe": (74, 8),
}

armors = {
    "None": (0, 0),
    "Leather": (13, 1),
    "Chainmail": (31, 2),
    "Splintmail": (53, 3),
    "Bandedmail": (75, 4),
    "Platemail": (102, 5),
}

rings = {
    "Left None": (0, 0, 0),
    "Right None": (0, 0, 0),
    "Damage +1": (25, 1, 0),
    "Damage +2": (50, 2, 0),
    "Damage +3": (100, 3, 0),
    "Defense +1": (20, 0, 1),
    "Defense +2": (40, 0, 2),
    "Defense +3": (80, 0, 3),
}

ring_pairs = combinations(rings.keys(), 2)

minimum_cost = sys.maxsize
maximum_cost = 0

for weapon, armor, (ring_a, ring_b) in product(weapons, armors, ring_pairs):

    weapon_cost, damage = weapons[weapon]
    armor_cost, defence = armors[armor]
    ring_a_cost, damage_boost_a, defence_boost_a = rings[ring_a]
    ring_b_cost, damage_boost_b, defence_boost_b = rings[ring_b]

    cost = weapon_cost + armor_cost + ring_a_cost + ring_b_cost
    damage += damage_boost_a + damage_boost_b
    defence += defence_boost_a + defence_boost_b

    my_rounds = math.ceil(boss_hp / max(1, (damage - boss_defence)))
    boss_rounds = math.ceil(my_hp / max(1, (boss_damage - defence)))

    if my_rounds <= boss_rounds and cost < minimum_cost:
        # print(weapon, armor, ring_a, ring_b, cost, damage, defence)
        minimum_cost = cost

    if my_rounds > boss_rounds and cost > maximum_cost:
        # print(weapon, armor, ring_a, ring_b, cost, damage, defence)
        maximum_cost = cost

print(f"Part 1: {minimum_cost}")
print(f"Part 2: {maximum_cost}")
