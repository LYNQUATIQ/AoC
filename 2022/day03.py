"""https://adventofcode.com/2022/day/3"""
import os
import string

with open(os.path.join(os.path.dirname(__file__), f"inputs/day03_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def solve(inputs: str) -> None:
    rucksacks = inputs.splitlines()

    dupes = []
    for rucksack in rucksacks:
        midpoint = len(rucksack) // 2
        compartment_1, compartment_2 = rucksack[:midpoint], rucksack[midpoint:]
        dupes += list(set(c for c in compartment_1 if c in compartment_2))
    print(f"\nPart 1: {sum(string.ascii_letters.index(c) + 1 for c in dupes)}")

    badges = []
    for i in range(0, len(rucksacks), 3):
        for c in string.ascii_letters:
            if all(c in pack for pack in rucksacks[i : i + 3]):
                badges.append(c)
    print(f"Part 2: {sum(string.ascii_letters.index(c) + 1 for c in badges)}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
