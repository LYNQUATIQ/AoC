"""https://adventofcode.com/2023/day/21"""
import os
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day21_input.txt")) as f:
    actual_input = f.read()


sample_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

ROCK = "#"
NORTH, SOUTH, EAST, WEST = 0 - 1j, 0 + 1j, 1 + 0j, -1 + 0j


def print_map(rocks, start, width, height, elves):
    for y in range(height):
        line = ""
        for x in range(width):
            xy = complex(x, y)
            c = "."
            if xy in rocks:
                c = ROCK
            if xy in elves:
                c = "O"
            if xy == start:
                c = "S"
            line += c
        print(line)
    print()


def solve(inputs: str, steps_to_take: int):
    rocks: set[complex] = set()
    for y, line in enumerate(inputs.splitlines()):
        for x, c in enumerate(line):
            if c == ROCK:
                rocks.add(complex(x, y))
    width, height = x + 1, y + 1
    start = complex(width // 2, height // 2)
    assert start not in rocks

    reached = defaultdict(set)
    reached[0] = set([start])
    for i in range(26_501_365):
        if i == steps_to_take:
            print(f"Part 1: {len(reached[i])}")
        for xy in reached[i]:
            for d in (NORTH, SOUTH, EAST, WEST):
                next_xy = xy + d
                if complex(next_xy.real % width, next_xy.imag % height) not in rocks:
                    reached[i + 1].add(next_xy)

    # for i in range(1, 4):
    #     print_map(rocks, start, width, height, reached[i])
    print(f"Part 2: {len(reached[26_501_365])}\n")


solve(sample_input, 6)
solve(actual_input, 64)
