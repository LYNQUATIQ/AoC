"""https://adventofcode.com/2022/day/4"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day04_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def solve(inputs: str) -> None:
    # values = tuple(map(int, inputs.splitlines()))
    lines = inputs.splitlines()
    assignments = []
    total1, total2 = 0, 0
    for line in lines:
        token1, token2 = line.split(",")
        a, b = map(int, token1.split("-"))
        c, d = map(int, token2.split("-"))
        assignments.append((a, b, c, d))
        if (a <= c and b >= d) or (c <= a and d >= b):
            total1 += 1
        if (b <= d and b >= c) or (d <= b and d >= a):
            total2 += 1

    print(f"\nPart 1: {total1}")
    print(f"Part 2: {total2}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
