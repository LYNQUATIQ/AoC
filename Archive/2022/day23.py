"""https://adventofcode.com/2022/day/23"""

import os

from itertools import cycle
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day23_input.txt")) as f:
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
    while round := round + 1:
        check_order = next(CHECK_ORDER)
        directions_to_check = [CHECKS[c] for c in check_order]
        proposals: defaultdict[complex, list[complex]] = defaultdict(list)
        for elf in elves:
            if not any((elf + d) in elves for d in (N, NE, E, SE, S, SW, W, NW)):
                continue
            for checks in directions_to_check:
                if not any((elf + d) in elves for d in checks):
                    proposals[elf + checks[0]].append(elf)
                    break

        elves_moved = False
        for new_position, (old_position, *other_elves) in proposals.items():
            if not other_elves:
                elves.remove(old_position)
                elves.add(new_position)
                elves_moved = True

        if round == 10:
            x_pos, y_pos = [int(e.real) for e in elves], [int(e.imag) for e in elves]
            y_pos = [int(elf.imag) for elf in elves]
            width, height = max(x_pos) - min(x_pos) + 1, max(y_pos) - min(y_pos) + 1
            print(f"Part 1: {width * height - len(elves)}")

        if not elves_moved:
            break

    print(f"Part 2: {round}\n")


solve(sample_input)
solve(actual_input)
