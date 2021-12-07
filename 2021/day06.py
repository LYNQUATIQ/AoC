import os

from collections import Counter, deque

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day06_input.txt")) as f:
    actual_input = f.read()

sample_input = """3,4,3,1,2"""


@print_time_taken
def solve(inputs):
    initial_fish = Counter(map(int, inputs.split(",")))
    fish = deque(initial_fish.get(i, 0) for i in range(9))

    for _ in range(80):
        fish.rotate(-1)
        fish[6] += fish[8]
    print(f"Part 1: {sum(fish)}")

    for _ in range(256 - 80):
        fish.rotate(-1)
        fish[6] += fish[8]
    print(f"Part 2: {sum(fish)}\n")


solve(sample_input)
solve(actual_input)
