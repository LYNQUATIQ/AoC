"""https://adventofcode.com/2023/day/6"""

import os
import re
import math

with open(os.path.join(os.path.dirname(__file__), "inputs/day06_input.txt")) as f:
    actual_input = f.read()


example_input = """Time:      7  15   30
Distance:  9  40  200"""


def ways_to_win(time: int, distance: int) -> int:
    root1 = (time + (time * time - 4 * distance) ** 0.5) / 2
    root2 = (time - (time * time - 4 * distance) ** 0.5) / 2
    root1 = root1 - 1 if root1 == int(root1) else root1
    return math.floor(root1) - math.floor(root2)


def solve(inputs: str):
    lines = inputs.splitlines()
    times = [int(n) for n in re.findall(r"\d+", lines[0])]
    distances = [int(n) for n in re.findall(r"\d+", lines[1])]

    wins = [ways_to_win(time, distance) for time, distance in zip(times, distances)]
    print(f"Part 1: {math.prod(wins)}")

    time = int("".join([str(n) for n in times]))
    distance = int("".join([str(n) for n in distances]))
    print(f"Part 2: {ways_to_win(time, distance)}\n")


solve(example_input)
solve(actual_input)
