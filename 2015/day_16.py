import logging
import os

import re

from itertools import combinations_with_replacement, permutations
from typing import NamedTuple

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

line_regex = re.compile(r"^Sue (?P<id>\d+): (?P<characteristics>[\w\d: ,]*)$")

sues = {}
for line in lines:
    params = line_regex.match(line).groupdict()
    characteristics = params["characteristics"].split(", ")
    sue_id = int(params["id"])
    sues[sue_id] = {}
    for characteristic in characteristics:
        k, v = tuple(characteristic.split(": "))
        sues[sue_id][k] = int(v)

known_characteristics = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


matched = None
for sue_id, sue_characteristics in sues.items():
    if any([known_characteristics[c] != v for c, v in sue_characteristics.items()]):
        continue
    matched = sue_id
    break

print(f"Part 1: {matched}")

exact_characteristics = {
    "children": 3,
    "samoyeds": 2,
    "akitas": 0,
    "vizslas": 0,
    "cars": 2,
    "perfumes": 1,
}
at_least_characteristics = {
    "cats": 7,
    "trees": 3,
}
at_most_characteristics = {
    "pomeranians": 3,
    "goldfish": 5,
}
matched = None
for sue_id, sue_characteristics in sues.items():
    if any([sue_characteristics.get(c, v) != v for c, v in exact_characteristics.items()]):
        continue
    if any([sue_characteristics.get(c, v + 1) <= v for c, v in at_least_characteristics.items()]):
        continue
    if any([sue_characteristics.get(c, v - 1) >= v for c, v in at_most_characteristics.items()]):
        continue
    matched = sue_id
    break

print(f"Part 2: {matched}")
