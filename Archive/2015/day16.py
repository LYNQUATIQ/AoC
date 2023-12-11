import os
import re

from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day16_input.txt")) as f:
    actual_input = f.read()

KNOWN_CHARACTERISTICS = {
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
AT_LEAST = ("cats", "trees")
AT_MOST = ("pomeranians", "goldfish")

REGEX = re.compile(r"^Sue (?P<id>\d+): (?P<characteristics>[\w\d: ,]*)$")


def match_sue(characteristics, at_least={}, at_most={}):
    if any(
        KNOWN_CHARACTERISTICS[c] >= characteristics.get(c, KNOWN_CHARACTERISTICS[c] + 1)
        for c in at_least
    ) or any(
        KNOWN_CHARACTERISTICS[c] <= characteristics.get(c, KNOWN_CHARACTERISTICS[c] - 1)
        for c in at_most
    ):
        return False
    to_match = set(characteristics.keys()) - set(at_least) - set(at_most)
    return all(KNOWN_CHARACTERISTICS[c] == characteristics[c] for c in to_match)


def solve(inputs):
    sues = defaultdict(dict)
    for data in (REGEX.match(line).groupdict() for line in inputs.splitlines()):
        for k, v in (tuple(x.split(": ")) for x in data["characteristics"].split(", ")):
            sues[int(data["id"])][k] = int(v)

    for sue_id, characteristics in sues.items():
        if match_sue(characteristics):
            print(f"Part 1: {sue_id}")

    for sue_id, characteristics in sues.items():
        if match_sue(characteristics, AT_LEAST, AT_MOST):
            print(f"Part 2: {sue_id}\n")


solve(actual_input)
