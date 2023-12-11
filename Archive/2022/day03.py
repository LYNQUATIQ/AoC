"""https://adventofcode.com/2022/day/3"""
import os
import string

with open(os.path.join(os.path.dirname(__file__), "inputs/day03_input.txt")) as f:
    actual_input = f.read()


sample_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def solve(inputs: str) -> None:
    packs = inputs.splitlines()

    dupes = []
    for pack in packs:
        midpoint = len(pack) // 2
        dupes += list(set(pack[:midpoint]) & set(pack[midpoint:]))
    print(f"Part 1: {sum(string.ascii_letters.index(c) + 1 for c in dupes)}")

    badges = []
    for i in range(0, len(packs), 3):
        badges += list(set(packs[i]) & set(packs[i + 1]) & set(packs[i + 2]))
    print(f"Part 2: {sum(string.ascii_letters.index(c) + 1 for c in badges)}\n")


solve(sample_input)
solve(actual_input)
