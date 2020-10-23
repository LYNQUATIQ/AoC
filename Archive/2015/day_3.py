import logging
import os

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

dir_dict = {"<": XY(-1, 0), "^": XY(0, -1), "v": XY(0, 1), ">": XY(1, 0)}

houses = defaultdict(int)
xy = XY(0, 0)
houses[xy] += 1
for c in lines[0]:
    xy += dir_dict[c]
    houses[xy] += 1

print(f"Part 1: {len(houses)}")

houses = defaultdict(int)
santa_xy = XY(0, 0)
robo_xy = XY(0, 0)
houses[santa_xy] += 1
houses[robo_xy] += 1
for i, c in enumerate(lines[0]):
    if i % 2:
        robo_xy += dir_dict[c]
        houses[robo_xy] += 1
    else:
        santa_xy += dir_dict[c]
        houses[santa_xy] += 1

print(f"Part 2: {len(houses)}")
