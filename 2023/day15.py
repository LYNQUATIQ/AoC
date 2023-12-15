"""https://adventofcode.com/2023/day/15"""
import os
from collections import defaultdict
from functools import reduce

with open(os.path.join(os.path.dirname(__file__), "inputs/day15_input.txt")) as f:
    actual_input = f.read()


sample_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def hash_value(token: str):
    return reduce(lambda value, x: (value + ord(x)) * 17 % 256, token, 0)


def solve(inputs: str):
    tokens = inputs.split(",")
    print(f"Part 1: {sum(hash_value(token) for token in tokens)}")

    boxes = defaultdict(dict)
    for token in tokens:
        if token.endswith("-"):
            label = token[:-1]
            boxes[hash_value(label)].pop(label, None)
        else:
            label, lens = token.split("=")
            boxes[hash_value(label)][label] = int(lens)
    focusing_power = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses.values(), 1):
            focusing_power += (box + 1) * i * lens
    print(f"Part 2: {focusing_power}\n")


solve(sample_input)
solve(actual_input)
