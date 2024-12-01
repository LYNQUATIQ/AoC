import logging
import os

import string

from collections import defaultdict
from grid_system import XY, ConnectedGrid

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

alphabet = lines[0].strip()
entry_points = {k: v for v, k in enumerate(alphabet, 1)}
mirrors = ConnectedGrid()
for y, line in enumerate(lines):
    for x, symbol in enumerate(line):
        mirrors.grid[XY(x, y)] = symbol

direction_switch = {
    "/": {
        mirrors.EAST: mirrors.NORTH,
        mirrors.NORTH: mirrors.EAST,
        mirrors.WEST: mirrors.SOUTH,
        mirrors.SOUTH: mirrors.WEST,
    },
    "\\": {
        mirrors.EAST: mirrors.SOUTH,
        mirrors.NORTH: mirrors.WEST,
        mirrors.WEST: mirrors.NORTH,
        mirrors.SOUTH: mirrors.EAST,
    },
}
mirror_flip = {"/": "\\", "\\": "/"}

plaintext = "FISSION_MAILED"
coded_text = ""
for symbol in plaintext:
    xy = XY(0, entry_points[symbol])
    direction = mirrors.EAST
    while True:
        xy += direction
        symbol = mirrors.grid[xy]
        if symbol in alphabet:
            coded_text += symbol
            break
        if symbol in ["/", "\\"]:
            direction = direction_switch[symbol][direction]
            mirrors.grid[xy] = mirror_flip[symbol]

print(coded_text)
