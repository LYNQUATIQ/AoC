"""https://adventofcode.com/2021/day/14"""

from collections import Counter
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day14_input.txt")) as f:
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
    template_polymer, rule_inputs = inputs.split("\n\n")
    insertion_rules = dict(tuple(r.split(" -> ")) for r in rule_inputs.splitlines())

    elements = Counter(template_polymer)
    pairs = Counter({pair: template_polymer.count(pair) for pair in insertion_rules})

    for step in range(40):
        for pair, occurences in dict(pairs).items():
            inserted_element = insertion_rules[pair]
            elements[inserted_element] += occurences
            pairs[pair[0] + inserted_element] += occurences
            pairs[inserted_element + pair[1]] += occurences
            pairs[pair] -= occurences
        if step == 9:
            print(f"Part 1: {max(elements.values()) - min(elements.values())}")

    print(f"Part 2: {max(elements.values()) - min(elements.values())}\n")


solve(sample_input)
solve(actual_input)
