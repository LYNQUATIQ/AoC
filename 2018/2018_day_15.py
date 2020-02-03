import logging
import os

from abc import ABC, abstractmethod
from collections import deque
from itertools import combinations, cycle
from typing import NamedTuple


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_15.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)


class Pt(NamedTuple("Pt", [("x", int), ("y", int)])):
    def __repr__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def order_key(self):
        return self.y * 10000 + self.x

    def neighbours(self):
        return [self + d for d in [Pt(0, 1), Pt(1, 0), Pt(0, -1), Pt(-1, 0)]]


class ElfDied(Exception):
    pass


class Unit:
    def __init__(self, species, loc, attack_power):
        self.hp = 200
        self.species = species
        self.loc = loc
        self.attack_power = attack_power

    def __repr__(self):
        return f"{self.species}@{int(self.loc.x)},{int(self.loc.y)}"

    def order_loc(self):
        return self.loc.order_key()

    def order_hp_loc(self):
        return self.hp * 10000000 + self.loc.order_key()

    @property
    def is_dead(self):
        return self.hp <= 0

    @property
    def is_alive(self):
        return self.hp > 0


class CaveSystem:

    WALL = "#"
    OPEN = "."
    GOBLIN = "G"
    ELF = "E"

    SPECIES = [GOBLIN, ELF]

    def __init__(self, lines, elf_power=3, stop_if_elf_is_dead=False):
        self.map = {}
        self.units = []
        self.round = 0
        self.stop_if_elf_is_dead = stop_if_elf_is_dead
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                loc = Pt(x, y)
                if c in self.SPECIES:
                    attack_power = 3
                    if c == self.ELF:
                        attack_power = elf_power
                    self.units.append(Unit(c, loc, attack_power))
                self.map[loc] = c
        self.max_x, self.max_y = x + 1, y + 1

    def connected_nodes(self, loc):
        return [n for n in loc.neighbours() if self.map[n] == self.OPEN]

    def survivors(self):
        return [u for u in self.units if u.is_alive]

    def targets(self, unit):
        return [u for u in self.survivors() if u.species != unit.species]

    def in_range_target(self, unit, targets):
        in_range_targets = [t for t in targets if t.loc in unit.loc.neighbours()]
        if not in_range_targets:
            return None
        return sorted(in_range_targets, key=lambda u: u.order_hp_loc())[0]

    def print_map(self):
        for y in range(self.max_y):
            row = ""
            units = []
            for x in range(self.max_x):
                row += self.map[(x, y)]
            row_units = [
                f"{u.species}({u.hp})"
                for u in sorted(self.survivors(), key=lambda u: u.order_loc())
                if u.loc.y == y
            ]
            row += "  " + ", ".join(row_units)
            print(row)
        print()

    def do_battle(self, debug=False):
        self.round = 0
        battle_over = False
        while not battle_over:
            battle_over = self.play_round()
            if debug:
                print(f"After {self.round} rounds:")
                self.print_map()
            self.round += 1

    def play_round(self):
        for unit in sorted(self.units, key=lambda u: u.order_loc()):
            if unit.is_alive:
                if self.make_move(unit):
                    return True

    def make_move(self, unit):
        targets = self.targets(unit)
        if not targets:
            return True
        target = self.in_range_target(unit, targets)

        # If no target then take a step
        if not target:
            self.take_step_towards_targets(unit, targets)
            target = self.in_range_target(unit, targets)

        # Attack neighbouring target
        if target:
            self.attack_target(unit, target)

    def attack_target(self, unit, target):
        target.hp -= unit.attack_power
        if target.hp <= 0:
            self.map[target.loc] = self.OPEN
            if self.stop_if_elf_is_dead and target.species == self.ELF:
                raise ElfDied()
        return None

    def take_step_towards_targets(self, unit, targets):
        # Get all the locations that are in range of targets
        potential_goals = set()
        for potential_target in targets:
            for loc in self.connected_nodes(potential_target.loc):
                potential_goals.add(loc)

        if not potential_goals:
            return

        best_path = self.shortest_path(unit.loc, potential_goals)
        if not best_path:
            return

        # Move along best path
        next_loc = best_path[0]
        self.map[unit.loc] = self.OPEN
        unit.loc = next_loc
        self.map[unit.loc] = unit.species

    def winning_species(self):
        return self.survivors()[0].species

    def outcome_summary(self):
        last_round = self.round - 1
        hp_sum = sum([u.hp for u in self.survivors()])
        answer = last_round * hp_sum
        print(f"After round: {last_round} - winners were {self.winning_species()}!")
        print(f"ANSWER: {last_round} x {hp_sum} ==> {answer}")
        return answer

    # Find the shortest path to the (closest of) goal(s)
    def shortest_path(self, start, goals, check_closest_neighbour=True):
        if isinstance(goals, Pt):
            goals = [goals]

        # List of points to visit (and their distance from the start)
        to_visit = deque([(start, 0)])
        visited = set()

        # Store path (from start) - for a node store distance, previous node (as tuple)
        paths = {start: (0, None)}
        # Get all the shortest paths
        while to_visit:
            this_node, distance_so_far = to_visit.popleft()
            for next_step in self.connected_nodes(this_node):
                if next_step not in paths or paths[next_step] > (
                    distance_so_far + 1,
                    this_node,
                ):
                    paths[next_step] = (distance_so_far + 1, this_node)
                if next_step in visited:
                    continue
                if next_step in [q for q, _ in to_visit]:
                    continue
                to_visit.append((next_step, distance_so_far + 1))
            visited.add(this_node)

        paths_to_goals = {node: path for node, path in paths.items() if node in goals}
        if not paths_to_goals:
            return None

        closest_goal = None
        shortest_distance = None
        for goal, (distance, _) in paths_to_goals.items():
            if closest_goal is None or distance < shortest_distance:
                closest_goal = goal
                shortest_distance = distance
                continue
            if distance > shortest_distance:
                continue
            if (
                distance == shortest_distance
                and goal.order_key() < closest_goal.order_key()
            ):
                closest_goal = goal
                shortest_distance = distance

        if check_closest_neighbour:
            best_nb_path = None
            for nb in sorted(self.connected_nodes(start), key=lambda u: u.order_key()):
                nb_path = self.shortest_path(
                    nb, closest_goal, check_closest_neighbour=False
                )
                if nb_path is None:
                    continue
                nb_path = [nb] + nb_path
                if best_nb_path is None:
                    best_nb_path = nb_path
                    continue
                if len(nb_path) < len(best_nb_path):
                    best_nb_path = nb_path
            path = best_nb_path
        else:
            path = [closest_goal]
            distance, node = paths[closest_goal]
            while distance > 1:
                path = [node] + path
                distance, node = paths[node]

        return path


for test in ["actual"]:
    # for test in [
    #     # "27730",
    #     "36334",
    #     "39514",
    #     "27755",
    #     "29844",
    #     "18740",
    # ]:
    print(f"Running test case: {test}\n-------------------------------")
    file_path = os.path.join(script_dir, f"inputs/2018_day15_input_{test}.txt")
    lines = [line.rstrip("\n") for line in open(file_path)]
    caves = CaveSystem(lines)
    caves.do_battle(debug=(test != "actual"))
    answer = caves.outcome_summary()
    if test != "actual":
        if int(test) == answer:
            print("SUCCESS :)\n")
        else:
            print("FAILURE :(\n")


for test in ["actual"]:
    # for test in [
    #     # "27730",
    #     "36334",
    #     "39514",
    #     "27755",
    #     "29844",
    #     "18740",
    # ]:
    print(f"Running test case: {test}\n-------------------------------")

    elves_win = False
    elf_attack_power = 14
    while not elves_win:
        elf_attack_power += 1
        file_path = os.path.join(script_dir, f"inputs/2018_day15_input_{test}.txt")
        lines = [line.rstrip("\n") for line in open(file_path)]
        caves = CaveSystem(lines, elf_attack_power, stop_if_elf_is_dead=True)
        try:
            caves.do_battle()
            break
        except ElfDied:
            pass
        print(f"{test}: ELves attack: {elf_attack_power} - got to round {caves.round}")
    caves.print_map()
    caves.outcome_summary()
    print(f"{test}: ELves attack: {elf_attack_power} - got to round {caves.round}")

