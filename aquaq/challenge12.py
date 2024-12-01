import logging
import os
import datetime
import math

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

instructions = {}
for floor, line in enumerate(lines):
    d, n = line.split()
    instructions[floor] = (not bool(int(d)), int(n))

floor = 0
direction = 1
visited = 0
while True:
    visited += 1
    try:
        change_direction, n = instructions[floor]
    except KeyError:
        break
    if change_direction:
        direction *= -1
    floor += n * direction

print(visited)
