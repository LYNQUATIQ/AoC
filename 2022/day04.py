"""https://adventofcode.com/2022/day/4"""
import os
import re

with open(os.path.join(os.path.dirname(__file__), f"inputs/day04_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def solve(inputs: str) -> None:
    part_1, part_2 = 0, 0
    for line in inputs.splitlines():
        a1, a2, b1, b2 = map(int, re.findall(r"\d+", line))
        if (a1 <= b1 <= b2 <= a2) or (b1 <= a1 <= a2 <= b2):
            part_1 += 1
        if not ((a1 > b2) or (b1 > a2)):
            part_2 += 1

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
