from collections import Counter
from functools import cache
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day14_input.txt")) as f:
    actual_input = f.read()

sample_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def solve(inputs):
    polymer, replacements = inputs.split("\n\n")
    replacements = dict(tuple(r.split(" -> ")) for r in replacements.splitlines())

    @cache
    def get_counts(a, b, steps):
        if not steps:
            return Counter()
        x = replacements[a + b]
        return Counter(x) + get_counts(a, x, steps - 1) + get_counts(x, b, steps - 1)

    def get_answer(steps):
        counts = Counter(polymer)
        for a, b in zip(polymer[:-1], polymer[1:]):
            counts += get_counts(a, b, steps)
        return max(counts.values()) - min(counts.values())

    print(f"Part 1: {get_answer(10)}")
    print(f"Part 2: {get_answer(40)}\n")


solve(sample_input)
solve(actual_input)
