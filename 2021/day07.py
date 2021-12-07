import os
import sys

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day07_input.txt")) as f:
    actual_input = f.read()

sample_input = """16,1,2,0,4,2,7,1,2,14"""


@print_time_taken
def solve(inputs):
    positions = list(map(int, inputs.split(",")))
    part1, part2 = sys.maxsize, sys.maxsize
    for x in range(min(positions), max(positions) + 1):
        distances = [abs(x - p) for p in positions]
        part1 = min(part1, sum(distances))
        part2 = min(part2, sum(d * (d + 1) // 2 for d in distances))
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
