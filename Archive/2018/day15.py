"""https://adventofcode.com/2018/day/15"""
import os

from collections import deque
from typing import NamedTuple

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day15_input.txt")) as f:
    actual_input = f.read()

sample_input = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""


class Pt(NamedTuple("Pt", [("x", int), ("y", int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return self.x < other.x if self.y == other.y else self.y < other.y

    def neighbours(self):
        return tuple(self + d for d in (Pt(0, -1), Pt(-1, 0), Pt(1, 0), Pt(0, 1)))


class ElfDied(Exception):
    pass


class Unit:
    def __init__(self, species, xy, attack_power):
        self.hp = 200
        self.species = species
        self.xy = xy
        self.attack_power = attack_power

    def __lt__(self, other):
        return self.xy < other.xy if self.hp == other.hp else self.hp < other.hp

    @property
    def is_alive(self):
        return self.hp > 0


class CaveSystem:

    WALL = "#"
    OPEN = "."
    GOBLIN = "G"
    ELF = "E"

    SPECIES = [GOBLIN, ELF]

    def __init__(self, inputs, elf_power=3, stop_if_elf_is_dead=False):
        self.map = {}
        self.units = set()
        self.round = 0
        self.stop_if_elf_is_dead = stop_if_elf_is_dead
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                xy = Pt(x, y)
                if c in self.SPECIES:
                    attack_power = 3
                    if c == self.ELF:
                        attack_power = elf_power
                    self.units.add(Unit(c, xy, attack_power))
                self.map[xy] = c

    def connected_nodes(self, xy):
        return (n for n in xy.neighbours() if self.map[n] == self.OPEN)

    def survivors(self):
        return {u for u in self.units if u.is_alive}

    def targets(self, unit):
        return {u for u in self.survivors() if u.species != unit.species}

    def in_range_target(self, unit, targets):
        in_range_targets = [t for t in targets if t.xy in unit.xy.neighbours()]
        if not in_range_targets:
            return None
        return sorted(in_range_targets)[0]

    def do_battle(self):
        self.round = 0
        while True:
            if self.play_round() == True:
                break
            self.round += 1
        return self.round * sum([u.hp for u in self.survivors()])

    def play_round(self):
        for unit in sorted(self.units, key=lambda x: x.xy):
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
            self.map[target.xy] = self.OPEN
            if self.stop_if_elf_is_dead and target.species == self.ELF:
                raise ElfDied()
        return None

    def take_step_towards_targets(self, unit, targets):
        # Get all the locations that are in range of targets
        potential_goals = set()
        for potential_target in targets:
            for xy in self.connected_nodes(potential_target.xy):
                potential_goals.add(xy)
        if not potential_goals:
            return
        best_path = self.shortest_path(unit.xy, potential_goals)
        if not best_path:
            return

        # Move along best path
        next_loc = best_path[0]
        self.map[unit.xy] = self.OPEN
        unit.xy = next_loc
        self.map[unit.xy] = unit.species

    def winning_species(self):
        return self.survivors()[0].species

    # Find the shortest path to the (closest of) goal(s)
    def shortest_path(self, start, goals, check_closest_neighbour=True):
        if isinstance(goals, Pt):
            goals = [goals]

        # List of points to visit (and their distance from the start)
        to_visit = deque([(start, 0)])
        visited = set()
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
            if distance == shortest_distance and goal < closest_goal:
                closest_goal = goal
                shortest_distance = distance

        if check_closest_neighbour:
            best_nb_path = None
            for nb in self.connected_nodes(start):
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


@print_time_taken
def solve(inputs):

    print(f"Part 1: {CaveSystem(inputs).do_battle()}")

    elf_attack_power = 14
    while True:
        elf_attack_power += 1
        caves = CaveSystem(inputs, elf_attack_power, stop_if_elf_is_dead=True)
        try:
            outcome = caves.do_battle()
            break
        except ElfDied:
            pass

    print(f"Part 2: {outcome}\n")


solve(sample_input)
# solve(actual_input)
