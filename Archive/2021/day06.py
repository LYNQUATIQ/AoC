"""https://adventofcode.com/2021/day/6"""
import os
from collections import Counter, deque

with open(os.path.join(os.path.dirname(__file__), "inputs/day06_input.txt")) as f:
    actual_input = f.read()

sample_input = """3,4,3,1,2"""


def solve(inputs):
    initial_fish = Counter(map(int, inputs.split(",")))
    fish = deque(initial_fish.get(i, 0) for i in range(9))

    for step in range(256):
        fish.rotate(-1)
        fish[6] += fish[8]
        if step == 79:
            print(f"Part 1: {sum(fish)}")
    print(f"Part 2: {sum(fish)}\n")


solve(sample_input)
solve(actual_input)
