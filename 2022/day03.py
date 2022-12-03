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
    dupes = []
    lines = inputs.splitlines()
    for line in lines:
        l = len(line) // 2
        pack1, pack2 = line[:l], line[l:]
        pack_dupes = set()
        for c in pack1:
            if c in pack2:
                pack_dupes.add(c)
        dupes += list(pack_dupes)
    total = 0
    for c in dupes:
        if c in string.ascii_lowercase:
            total += ord(c) - ord("a") + 1
        else:
            total += ord(c) - ord("A") + 27
    print(f"\nPart 1: {total}")

    badges = []
    for i in range(0, len(lines), 3):
        pack1, pack2, pack3 = lines[i], lines[i + 1], lines[i + 2]
        for c in string.ascii_letters:
            if c in pack1 and c in pack2 and c in pack3:
                badges.append(c)
                break
    total = 0
    for c in badges:
        if c in string.ascii_lowercase:
            total += ord(c) - ord("a") + 1
        else:
            total += ord(c) - ord("A") + 27
    print(f"Part 2: {total}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
