import os
import re

from collections import defaultdict
from itertools import product
from grid_system import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

TOG, ON, OFF = "toggle", "turn on", "turn off"
regex = re.compile(
    rf"^(?P<phrase>({TOG})|({ON})|({OFF})) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)$"
)


def solve(inputs):
    instructions = (regex.match(line).groupdict() for line in inputs.splitlines())

    lights1, lights2 = defaultdict(bool), defaultdict(int)
    for instruction in instructions:
        x_range = range(int(instruction["x1"]), int(instruction["x2"]) + 1)
        y_range = range(int(instruction["y1"]), int(instruction["y2"]) + 1)
        for xy in (XY(x, y) for x, y in product(x_range, y_range)):
            phrase = instruction["phrase"]
            lights1[xy] = {TOG: not lights1[xy], ON: True, OFF: False}[phrase]
            lights2[xy] += {TOG: 2, ON: 1, OFF: -1}[phrase]
            lights2[xy] = max(lights2[xy], 0)

    print(f"Part 1: {sum(lights1.values())}")
    print(f"Part 2: {sum(lights2.values())}")


solve(actual_input)