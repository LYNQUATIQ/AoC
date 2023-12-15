"""https://adventofcode.com/2023/day/15"""
import os
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day15_input.txt")) as f:
    actual_input = f.read()


sample_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def hash_value(token: str):
    value = 0
    for c in token:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def solve(inputs: str):
    tokens = inputs.split(",")

    value = 0
    for token in tokens:
        h = hash_value(token)
        # print(token, h)
        value += h
    print(f"Part 1: {value}")

    boxes = defaultdict(dict)
    for token in tokens:
        if token.endswith("-"):
            label = token[:-1]
            box = hash_value(label)
            boxes[box].pop(label, None)
        else:
            label, lens = token.split("=")
            box = hash_value(label)
            boxes[box][label] = int(lens)
    value = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses.values(), 1):
            value += (box + 1) * i * lens
    print(f"Part 2: {value}\n")


solve(sample_input)
solve(actual_input)
