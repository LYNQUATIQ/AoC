import logging
import os

import re

from collections import defaultdict

from grid_system import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

regex = re.compile(
    r"^(?P<instruction>(toggle)|(turn on)|(turn off)) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)$"
)
directions = [regex.match(line).groupdict() for line in lines]

lights = defaultdict(bool)
for direction in directions:
    instruction = direction["instruction"]
    x_range = range(int(direction["x1"]), int(direction["x2"]) + 1)
    y_range = range(int(direction["y1"]), int(direction["y2"]) + 1)
    for y in y_range:
        for x in x_range:
            xy = XY(x, y)
            lights[xy] = {"toggle": not lights[xy], "turn on": True, "turn off": False}[
                instruction
            ]
print(f"Part 1: {sum(lights.values())}")

lights = defaultdict(int)
for direction in directions:
    instruction = direction["instruction"]
    x_range = range(int(direction["x1"]), int(direction["x2"]) + 1)
    y_range = range(int(direction["y1"]), int(direction["y2"]) + 1)
    for y in y_range:
        for x in x_range:
            xy = XY(x, y)
            lights[xy] += {"toggle": 2, "turn on": 1, "turn off": -1}[instruction]
            lights[xy] = max(lights[xy], 0)
print(f"Part 2: {sum(lights.values())}")
