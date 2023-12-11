"""https://adventofcode.com/2018/day/5"""
import os
import re
import string
import sys

from collections import deque


with open(os.path.join(os.path.dirname(__file__), "inputs/day05_input.txt")) as f:
    actual_input = f.read()

sample_input = """dabAcCaCBAcCcaDA"""


def reduce_polymer(polymer):
    reduction = deque()
    i = 0
    while i < len(polymer):
        try:
            a, b = reduction[-1], polymer[i]
        except IndexError:
            reduction = deque(polymer[i])
            i += 1
            continue
        if a.lower() == b.lower() and a != b:
            reduction.pop()
        else:
            reduction += b
        i += 1
    return reduction


def solve(inputs):
    reduction = reduce_polymer(inputs)
    print(f"Part 1: {len(reduction)}")

    best_reduction = sys.maxsize
    for c in string.ascii_lowercase:
        polymer = re.sub(c, "", inputs, flags=re.IGNORECASE)
        best_reduction = min(best_reduction, len(reduce_polymer(polymer)))
    print(f"Part 2: {best_reduction}\n")


solve(sample_input)
solve(actual_input)
