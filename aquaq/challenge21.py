import logging
import os

import datetime

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

width = 20
vac_width = 5
positions = width - vac_width + 1
max_motes = [0] * positions
for line in lines:
    tiles = [int(x) for x in line.split()]
    new_max_motes = []
    for i in range(positions):
        prior_max = [max_motes[i]]
        if i > 0:
            prior_max.append(max_motes[i - 1])
        if i < positions - 1:
            prior_max.append(max_motes[i + 1])
        new_max_motes.append(sum(tiles[i : i + vac_width]) + max(prior_max))
    max_motes = new_max_motes
    print(max_motes)

print(max(max_motes))
