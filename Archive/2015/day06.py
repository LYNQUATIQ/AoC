import os
import re

from collections import defaultdict
from itertools import product

with open(os.path.join(os.path.dirname(__file__), "inputs/day06_input.txt")) as f:
    actual_input = f.read()

TOG, ON, OFF = "toggle", "turn on", "turn off"
regex = re.compile(
    rf"^(?P<phrase>({TOG})|({ON})|({OFF})) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)$"
)


def solve(inputs):
    instructions = (regex.match(line).groupdict() for line in inputs.splitlines())
    part1, part2 = defaultdict(bool), defaultdict(int)
    for instruction in instructions:
        x_range = range(int(instruction["x1"]), int(instruction["x2"]) + 1)
        y_range = range(int(instruction["y1"]), int(instruction["y2"]) + 1)
        phrase = instruction["phrase"]
        for xy in product(x_range, y_range):
            part1[xy] = {TOG: not part1[xy], ON: True, OFF: False}[phrase]
            part2[xy] += {TOG: 2, ON: 1, OFF: -1 if part2[xy] else 0}[phrase]

    print(f"Part 1: {sum(part1.values())}")
    print(f"Part 2: {sum(part2.values())}\n")


solve(actual_input)
