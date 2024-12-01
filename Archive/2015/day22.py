import logging
import os

import copy
import sys

from collections import deque


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="w",
)

boss_hp = 71
boss_damage = 10

my_hp = 50
mana = 500

# Cost, immediate damage, immediate hp
spells = {
    "Magic Missile": (53, 4, 0),
    "Drain": (73, 2, 2),
    "Shield": (113, 0, 0),
    "Poison": (173, 0, 0),
    "Recharge": (229, 0, 0),
}

effects = ["Shield", "Poison", "Recharge"]

# Turns, effect
effect_turns = {
    "Shield": 6,
    "Poison": 6,
    "Recharge": 5,
}

# Turns, hp effect, damage effect, mana effect
effect_impact = {
    "Shield": (7, 0, 0),
    "Poison": (0, 3, 0),
    "Recharge": (0, 0, 101),
}


class BattleState:
    def __init__(
        self,
        boss_hp,
        hp,
        mana,
        effect_timers={e: 0 for e in effects},
        turns=0,
        mana_spend=0,
    ):
        self.boss_hp = boss_hp
        self.my_hp = my_hp
        self.mana = mana
        self.effect_timers = effect_timers
        self.turns = turns
        self.mana_spend = mana_spend


def minimum_spend(hp_loss=0):
    states_to_visit = deque([BattleState(boss_hp, my_hp, mana)])
    minimum_spend = sys.maxsize
    while states_to_visit:

        state = states_to_visit.popleft()

        player_turn = state.turns % 2 == 0
        state.turns += 1

        armor = 0
        for effect in effects:
            if state.effect_timers[effect] > 0:
                hp_effect, damage_effect, mana_effect = effect_impact[effect]
                armor += hp_effect
                state.boss_hp -= damage_effect
                state.mana += mana_effect
                state.effect_timers[effect] -= 1

        if state.boss_hp <= 0:
            if state.mana_spend < minimum_spend:
                minimum_spend = state.mana_spend
            continue

        if not player_turn:
            state.my_hp -= max(1, (boss_damage - armor))
            if state.my_hp > 0:
                states_to_visit.append(state)
            continue

        state.my_hp -= hp_loss
        if state.my_hp <= 0:
            continue

        for spell, (cost, damage, hp) in spells.items():
            if cost > state.mana:
                continue
            if state.mana_spend + cost > minimum_spend:
                continue
            if state.effect_timers.get(spell, 0) > 0:
                continue
            new_state = copy.deepcopy(state)
            new_state.mana -= cost
            new_state.mana_spend += cost
            new_state.my_hp += hp
            new_state.boss_hp -= damage
            if new_state.boss_hp <= 0:
                if new_state.mana_spend < minimum_spend:
                    minimum_spend = new_state.mana_spend
                continue
            try:
                new_state.effect_timers[spell] = effect_turns[spell]
            except KeyError:
                pass
            states_to_visit.append(new_state)

    return minimum_spend


print(f"Part 1: {minimum_spend()}")
print(f"Part 2: {minimum_spend(1)}")
