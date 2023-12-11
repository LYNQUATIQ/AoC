"""https://adventofcode.com/2022/day/1"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day01_input.txt")) as f:
    actual_input = f.read()


sample_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def solve(inputs: str) -> None:
    calories = [sum(map(int, elf.splitlines())) for elf in inputs.split("\n\n")]
    calories.sort(reverse=True)

    print(f"Part 1: {calories[0]}")
    print(f"Part 2: {sum(calories[0:3])}\n")


solve(sample_input)
solve(actual_input)
