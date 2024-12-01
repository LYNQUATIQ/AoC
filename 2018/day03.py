"""https://adventofcode.com/2018/day/3"""

import os
import re

from collections import defaultdict
from itertools import product

with open(os.path.join(os.path.dirname(__file__), "inputs/day03_input.txt")) as f:
    actual_input = f.read()

sample_input = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""

REGEX = r"^#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)$"


def solve(inputs):
    cloth = defaultdict(int)
    claims = {}

    for line in inputs.splitlines():
        claim = {k: int(v) for k, v in re.match(REGEX, line).groupdict().items()}
        x, y, w, h = claim["x"], claim["y"], claim["w"], claim["h"]
        claims[claim["id"]] = (x, y, w, h)
        for xd, yd in product(range(w), range(h)):
            cloth[(x + xd, y + yd)] += 1
    print(f"Part 1: {sum(c > 1 for c in cloth.values())}")

    for claim_id, (x, y, w, h) in claims.items():
        if all(cloth[(x + xd, y + yd)] == 1 for xd, yd in product(range(w), range(h))):
            break
    print(f"Part 2: {claim_id}\n")


solve(sample_input)
solve(actual_input)
