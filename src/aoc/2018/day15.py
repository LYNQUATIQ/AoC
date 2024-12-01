"""https://adventofcode.com/2018/day/15"""

import os

from collections import deque
from dataclasses import dataclass
from typing import NamedTuple

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), "inputs/day15_input.txt")) as f:
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

ELF, GOBLIN = "E", "G"


class Pt(NamedTuple("Pt", [("x", int), ("y", int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return self.x < other.x if self.y == other.y else self.y < other.y

    @property
    def neighbours(self):
        return tuple(self + d for d in (Pt(0, -1), Pt(-1, 0), Pt(1, 0), Pt(0, 1)))


@dataclass
class Unit:
    species: str
    hp: int = 200
    power: int = 3


class ElfDied(Exception):
    pass


class Caves:
    WALL = "#"

    def __init__(self, inputs, elf_power=3):
        self.map = set()
        self.units = {}
        for y, line in enumerate(inputs.splitlines()):
            for x, c in enumerate(line):
                xy = Pt(x, y)
                if c == self.WALL:
                    self.map.add(xy)
                if c in [GOBLIN, ELF]:
                    self.units[xy] = Unit(c, power=elf_power if c == ELF else 3)

    def do_battle(self, raise_elf_death: bool = False):
        rounds = 0
        while True:
            for unit_xy in sorted(self.units):
                try:
                    unit = self.units[unit_xy]
                except:
                    continue  # unit was killed earlier in round
                targets = {
                    xy for xy, t in self.units.items() if unit.species != t.species
                }
                if not targets:  # Combat's over... all opponents defeated
                    return rounds * sum(u.hp for u in self.units.values())
                self.make_move(unit_xy, unit, targets, raise_elf_death)
            rounds += 1

    def make_move(
        self, unit_xy: Pt, unit: Unit, targets: set[Pt], raise_elf_death: bool
    ):
        opponents = {t for t in targets if t in unit_xy.neighbours}
        if not opponents:
            in_range = {
                xy
                for target_xy in targets
                for xy in target_xy.neighbours
                if xy not in self.map and xy not in self.units
            }
            new_xy = self.find_move(unit_xy, in_range)
            if new_xy:
                self.units[new_xy] = self.units.pop(unit_xy)
                opponents = {t for t in targets if t in new_xy.neighbours}

        if opponents:
            target_xy, target = sorted(
                ((xy, self.units[xy]) for xy in opponents),
                key=lambda x: (x[1].hp, x[0]),
            )[0]
            target.hp -= unit.power
            if target.hp <= 0:
                if target.species == ELF and raise_elf_death:
                    raise ElfDied()
                del self.units[target_xy]

    def find_move(self, start, targets):
        to_visit = deque([(start, 0)])
        occupied = {xy for xy in self.units if xy != start}
        paths = {start: (0, None)}
        visited = set()
        while to_visit:
            xy, distance = to_visit.popleft()
            for n in xy.neighbours:
                if n in self.map or n in occupied:
                    continue
                if n not in paths or paths[n] > (distance + 1, xy):
                    paths[n] = (distance + 1, xy)
                if n in visited:
                    continue
                if not any(n == v[0] for v in to_visit):
                    to_visit.append((n, distance + 1))
            visited.add(xy)

        try:
            _, closest_target = min(
                (d, xy) for xy, (d, _) in paths.items() if xy in targets
            )
        except ValueError:
            return None

        distances, to_visit = {closest_target: 0}, deque([(closest_target, 0)])
        while to_visit:
            xy, distance = to_visit.popleft()
            if xy == start:
                break
            for n in xy.neighbours:
                if not (n in self.map or n in occupied or n in distances):
                    distances[n] = distance + 1
                    to_visit.append((n, distance + 1))

        _, best_move = min(
            (d, xy) for xy, d in distances.items() if xy in start.neighbours
        )
        return best_move


@print_time_taken
def solve(inputs):
    print(f"Part 1: {Caves(inputs).do_battle()}")

    definitely_lose, definitely_win = 3, 200
    while True:
        candidate = (definitely_win - definitely_lose) // 2 + definitely_lose
        try:
            outcome = Caves(inputs, candidate).do_battle(raise_elf_death=True)
        except ElfDied:
            definitely_lose = candidate
            continue
        definitely_win = candidate
        if definitely_win == definitely_lose + 1:
            break
    print(f"Part 2: {outcome}\n")


solve(sample_input)
solve(actual_input)
