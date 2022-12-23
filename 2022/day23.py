"""https://adventofcode.com/2022/day/23"""
import os

from itertools import cycle
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), f"inputs/day23_input.txt")) as f:
    actual_input = f.read()


sample_input = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""


N, NE, E, SE = 0 - 1j, +1 - 1j, +1 + 0j, +1 + 1j
S, SW, W, NW = 0 + 1j, -1 + 1j, -1 + 0j, -1 - 1j

CHECK_ORDER = cycle([(N, S, W, E), (S, W, E, N), (W, E, N, S), (E, N, S, W)])
CHECKS = {N: (N, NE, NW), S: (S, SE, SW), W: (W, NW, SW), E: (E, NE, SE)}


def solve(inputs: str) -> None:

    elves: set[complex] = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            if c == "#":
                elves.add(complex(x, y))

    round = 0
    states: set[frozenset[complex]] = set()
    while True:
        round += 1
        check_order = next(CHECK_ORDER)
        directions = [d for d in (CHECKS[c] for c in check_order)]
        proposals: defaultdict[complex, list[complex]] = defaultdict(list)
        for elf in elves:
            if not any((elf + d) in elves for d in (N, NE, E, SE, S, SW, W, NW)):
                continue
            for checks in directions:
                if not any((elf + d) in elves for d in checks):
                    proposals[elf + checks[0]].append(elf)
                    break
        for proposal, movers in proposals.items():
            if len(movers) == 1:
                elf = movers[0]
                elves.remove(elf)
                elves.add(proposal)

        if round == 10:
            min_x, max_x = float("inf"), float("-inf")
            min_y, max_y = float("inf"), float("-inf")
            for elf in elves:
                x, y = int(elf.real), int(elf.imag)
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
            x_extent = max_x - min_x + 1
            y_extent = max_y - min_y + 1
            print(f"Part 1: {x_extent * y_extent - len(elves)}")
            break

    print(f"Part 2: {False}\n")


solve(sample_input)
# solve(actual_input)
