import os
import re

from collections import defaultdict

from grid_system import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

directions = {"U": XY(0, -1), "D": XY(0, 1), "R": XY(1, 0), "L": XY(-1, 0)}

wires = defaultdict(dict)
for i, line in enumerate(lines):
    xy, steps = XY(0, 0), 0
    for direction, distance in re.findall(r"([U|D|L|R])(\d+)", line):
        for d in range(int(distance)):
            xy += directions[direction]
            steps += 1
            wires[i][xy] = steps

intersections = set(wires[0]).intersection(set(wires[1]))
print(f"Part 1: {min(xy.manhattan_distance for xy in intersections)}")
print(f"Part 2: {min(wires[0][xy]+wires[1][xy] for xy in intersections)}")
