"""https://adventofcode.com/2018/day/24"""
import os
import re

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day24_input.txt")) as f:
    actual_input = f.read()

sample_input = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""

REGEX = re.compile(
    r"^(?P<units>\d+) unit[s?] each with (?P<hp>\d+) hit point[s?] (\((?P<weaknesses_immunities>.+)\) )?with an attack that does (?P<damage>\d+) (?P<attack>\w+) damage at initiative (?P<initiative>\d+)$"
)
FEATURE_REGEX = re.compile(r"^(?P<weak_immune>weak|immune) to (?P<features>.+)$")


class ArmyGroup:
    def __init__(self, data: str, boost: int = 0) -> None:
        matches = REGEX.match(data).groupdict()
        self.units = int(matches["units"])
        self.hp = int(matches["hp"])
        self.initiative = int(matches["initiative"])
        self.damage = int(matches["damage"]) + boost
        self.attack = matches["attack"]
        self.weaknesses, self.immunities = tuple(), tuple()
        if matches["weaknesses_immunities"]:
            for weakness_immunity in matches["weaknesses_immunities"].split("; "):
                feature_match = FEATURE_REGEX.match(weakness_immunity)
                features = tuple(feature_match["features"].split(", "))
                if feature_match["weak_immune"] == "weak":
                    self.weaknesses = features
                else:
                    self.immunities = features

    @property
    def effective_power(self):
        return self.units * self.damage

    def damage_taken(self, attacker):
        multiplier = 1
        if attacker.attack in self.weaknesses:
            multiplier = 2
        if attacker.attack in self.immunities:
            multiplier = 0
        return attacker.effective_power * multiplier

    def attacked(self, attacker):
        self.units -= self.damage_taken(attacker) // self.hp


def battle_result(inputs: str, immune_boost: int = 0) -> tuple[int, int]:
    immune_inputs, infection_inputs = inputs.split("\n\n")
    immune_system = {ArmyGroup(l, immune_boost) for l in immune_inputs.splitlines()[1:]}
    infection = {ArmyGroup(l) for l in infection_inputs.splitlines()[1:]}

    remaining_units = sum(max(u.units, 0) for u in immune_system) + sum(
        max(u.units, 0) for u in infection
    )
    while True:
        targets = {}
        all_units = (g for g in immune_system | infection if g.units > 0)
        for unit in sorted(
            all_units, key=lambda x: (x.effective_power, x.initiative), reverse=True
        ):
            other_team = immune_system if unit in infection else infection
            potential_targets = sorted(
                (u for u in other_team if u.units > 0 and u not in targets.values()),
                key=lambda x: (x.damage_taken(unit), x.effective_power, x.initiative),
                reverse=True,
            )
            if potential_targets:
                potential_target = potential_targets[0]
                if potential_target.damage_taken(unit) > 0:
                    targets[unit] = potential_target

        for attacker in sorted(targets, key=lambda x: x.initiative, reverse=True):
            if attacker.units > 0:
                targets[attacker].attacked(attacker)

        immune_remaining_units = sum(max(u.units, 0) for u in immune_system)
        infection_remaining_units = sum(max(u.units, 0) for u in infection)
        if immune_remaining_units + infection_remaining_units == remaining_units:
            return 0, 0  # Stalemate
        remaining_units = immune_remaining_units + infection_remaining_units

        if immune_remaining_units == 0 or infection_remaining_units == 0:
            return immune_remaining_units, infection_remaining_units


@print_time_taken
def solve(inputs):
    _, infection = battle_result(inputs)
    print(f"Part 1:{infection}")

    definitely_lose, definitely_win, immune_win = 0, infection * 20, 0
    while True:
        if definitely_win == definitely_lose + 1:
            break
        boost = (definitely_win - definitely_lose) // 2 + definitely_lose
        immune, _ = battle_result(inputs, boost)
        if immune == 0:
            definitely_lose = boost
            continue
        definitely_win, immune_win = boost, immune
    print(f"Part 2: {immune_win}\n")


solve(sample_input)
solve(actual_input)
