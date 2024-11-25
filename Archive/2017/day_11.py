import logging
import os

from grid_system import XY


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_11.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_11_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
assert len(lines) == 1
path = lines[0].split(",")

directions = {
    "n": XY(0, 2),
    "ne": XY(1, 1),
    "se": XY(1, -1),
    "s": XY(0, -2),
    "sw": XY(-1, -1),
    "nw": XY(-1, 1),
}


def distance(target):
    x, y = abs(target.x), abs(target.y)
    if x < y:
        return x + (y - x) // 2
    return x


start = XY(0, 0)
target = XY(0, 0)
max_distance = 0
for step in path:
    target += directions[step]
    max_distance = max(max_distance, distance(target))

print(f"Part 1: {distance(target)}")
print(f"Part 1: {max_distance}")
