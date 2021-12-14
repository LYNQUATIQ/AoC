from collections import Counter
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
    template_polymer, replacements = inputs.split("\n\n")
    replacements = dict(tuple(r.split(" -> ")) for r in replacements.splitlines())

    elements = Counter(template_polymer)
    pairs = Counter({pair: template_polymer.count(pair) for pair in replacements})
    for step in range(40):
        for pair, occurences in pairs.copy().items():
            replacement = replacements[pair]
            elements[replacement] += occurences
            pairs[pair] -= occurences
            pairs[pair[0] + replacement] += occurences
            pairs[replacement + pair[1]] += occurences
        if step == 9:
            print(f"Part 1: {max(elements.values()) - min(elements.values())}")

    print(f"Part 2: {max(elements.values()) - min(elements.values())}\n")


solve(sample_input)
solve(actual_input)
