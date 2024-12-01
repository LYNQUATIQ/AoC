"""https://adventofcode.com/2018/day/2"""

import os

from collections import Counter
from itertools import combinations

with open(os.path.join(os.path.dirname(__file__), "inputs/day02_input.txt")) as f:
    actual_input = f.read()

sample_input1 = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

sample_input2 = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""


def solve(inputs):
    box_ids = inputs.splitlines()

    counts = [Counter(box_id) for box_id in box_ids]
    twos = sum(2 in count.values() for count in counts)
    threes = sum(3 in count.values() for count in counts)
    print(f"Part 1: {twos * threes}")

    for a, b in combinations(box_ids, 2):
        differences = [i for i, c in enumerate(a) if b[i] != c]
        if len(differences) == 1:
            break
    print(f"Part 2: {a[:differences[0]] + a[differences[0]+1:]}\n")


solve(sample_input1)
solve(sample_input2)
solve(actual_input)
