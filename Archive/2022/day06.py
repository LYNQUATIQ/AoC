"""https://adventofcode.com/2022/day/6"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day06_input.txt")) as f:
    actual_input = f.read()


sample_input = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


def find_marker(datastream: str, length: int) -> int:
    i = length
    while len(set(datastream[i - length : i])) < length:
        i += 1
    return i


def solve(datastream: str) -> None:
    print(f"Part 1: {find_marker(datastream, 4)}")
    print(f"Part 2: {find_marker(datastream, 14)}\n")


solve(sample_input)
solve(actual_input)
