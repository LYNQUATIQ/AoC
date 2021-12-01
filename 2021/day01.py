import os

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day01_input.txt")) as f:
    actual_input = f.read()

sample_input = """199
200
208
210
200
207
240
269
260
263"""


@print_time_taken
def solve(inputs):
    values = list(map(int, inputs.splitlines()))
    print(f"Part 1: {sum(a < b for a, b in zip(values[:-1], values[1:]))}")

    values = [a + b + c for a, b, c in zip(values[:-2], values[1:-1], values[2:])]
    print(f"Part 2: {sum(a < b for a, b in zip(values[:-1], values[1:]))}")


solve(sample_input)
solve(actual_input)
