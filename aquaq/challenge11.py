import logging
import os
import datetime
import math

from collections import defaultdict
from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

areas = []
for line in lines:
    lx, ly, ux, uy = line.split(",")
    areas.append((int(lx), int(ly), int(ux), int(uy)))

floor = defaultdict(int)
# Lay the tiles
for lx, ly, ux, uy in areas:
    for x in range(lx, ux):
        for y in range(ly, uy):
            floor[(x, y)] += 1

# Remove unconnected areas
for lx, ly, ux, uy in areas:
    unconnected = True
    for x in range(lx, ux):
        for y in range(ly, uy):
            if floor[(x, y)] > 1:
                unconnected = False
    if unconnected:
        for x in range(lx, ux):
            for y in range(ly, uy):
                floor[(x, y)] = 0

print(sum(map(bool, floor.values())))
