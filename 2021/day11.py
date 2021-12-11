# import logging
import math
import os

from collections import defaultdict

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day11_input.txt")) as f:
    actual_input = f.read()

sample_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


@print_time_taken
def solve(inputs):
    octopi_grid = {
        (x, y): int(octopus)
        for y, line in enumerate(inputs.splitlines())
        for x, octopus in enumerate(line)
    }
    octopi = {i: set() for i in range(11)}
    for xy, level in octopi_grid.items():
        octopi[level].add(xy)

    # print_octopi(octopi)
    get_neighbours = lambda x, y: (
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1),
        (x - 1, y + 1),
        (x - 1, y),
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
    )

    flashes, step = 0, 0
    while True:
        step += 1
        octopi = {(level + 1) % 11: xys for level, xys in octopi.items()}
        flashed = set()
        while octopi[10]:
            octopus = octopi[10].pop()
            octopi[0].add(octopus)
            if octopus in flashed:
                continue
            flashes += 1
            flashed.add(octopus)
            for neighbour in get_neighbours(*octopus):
                current_level = None
                for neighbour_level, xys in octopi.items():
                    if neighbour in xys:
                        current_level = neighbour_level
                        break
                if current_level is not None and current_level > 0:
                    octopi[current_level].remove(neighbour)
                    octopi[min(current_level + 1, 10)].add(neighbour)
        if step == 100:
            print(f"Part 1: {flashes}")
        if len(flashed) == 100:
            break
    print(f"Part 2: {step}\n")


solve(sample_input)
solve(actual_input)
