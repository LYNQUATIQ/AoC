import os

from itertools import product

from grid import XY
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


class Octopi:
    def __init__(self, inputs):
        self.octopi = {}
        for y, line in enumerate(inputs.splitlines()):
            for x, level in enumerate(line):
                self.octopi[XY(x, y)] = int(level)
        self.bounds = XY(x, y)

    def flashing_octopus(self):
        for octopus, level in self.octopi.items():
            if level > 9:
                return octopus
        return None

    def octopus_neighbours(self, octopus):
        return (n for n in octopus.all_neighbours if n.in_bounds(self.bounds))

    def take_step(self):
        for octopus, level in self.octopi.items():
            self.octopi[octopus] = level + 1

        flashed = set()
        while flasher := self.flashing_octopus():
            self.octopi[flasher] = 0
            flashed.add(flasher)
            for neighbour in self.octopus_neighbours(flasher):
                if neighbour not in flashed:
                    self.octopi[neighbour] += 1

        return len(flashed)


@print_time_taken
def solve(inputs):
    octopi = Octopi(inputs)

    flashes, step = 0, 0
    while True:
        step += 1
        flashed = octopi.take_step()
        flashes += flashed
        if step == 100:
            print(f"Part 1: {flashes}")
        if flashed == 100:
            print(f"Part 2: {step}\n")
            break


solve(sample_input)
solve(actual_input)
