"""https://adventofcode.com/2022/day/1"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day01_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """1000
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

    print(f"\nPart 1: {calories[0]}")
    print(f"Part 2: {sum(calories[0:3])}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
