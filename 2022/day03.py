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

PRIORITIES = {c: i for i, c in enumerate(string.ascii_lowercase, 1)} | {
    c: i for i, c in enumerate(string.ascii_uppercase, 27)
}


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


def solve(inputs: str) -> None:
    rucksacks = inputs.splitlines()

    dupes = []
    for rucksack in rucksacks:
        midpoint = len(rucksack) // 2
        compartment_1, compartment_2 = rucksack[:midpoint], rucksack[midpoint:]
        dupes += list(set(c for c in compartment_1 if c in compartment_2))
    print(f"\nPart 1: {sum(map(PRIORITIES.get, dupes))}")

    badges = []
    for pack1, pack2, pack3 in grouper(rucksacks, 3):
        for c in string.ascii_letters:
            if c in pack1 and c in pack2 and c in pack3:
                badges.append(c)
                break
    print(f"Part 2: {sum(map(PRIORITIES.get, badges))}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
