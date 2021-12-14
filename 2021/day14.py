# import logging
import math
import os
import re
import string
import sys

from functools import lru_cache
from collections import defaultdict, Counter
from itertools import product
from typing import Iterator

from grid import XY, ConnectedGrid
from utils import flatten, grouper, powerset, print_time_taken

# log_file = os.path.join(os.path.dirname(__file__), f"logs/day14.log")
# logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")
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


@print_time_taken
def solve(inputs):
    input_polymer, b = inputs.split("\n\n")
    replacements = {}
    for x in b.splitlines():
        k, v = x.split(" -> ")
        replacements[k] = v

    def do_r(p):
        n = ""
        for i, j in zip(p[:-1], p[1:]):
            insert = replacements.get(i + j, "")
            n += i + insert
        return n + p[-1]

    polymer = input_polymer
    for i in range(10):
        polymer = do_r(polymer)
    counts = Counter(polymer).values()
    print(f"Part 1: {max(counts)-min(counts)}")

    cache = {}

    def get_counts(a, b, iterations):
        if not iterations:
            return {}
        try:
            return cache[(a, b, iterations)]
        except KeyError:
            pass
        insert = replacements[a + b]
        counts = defaultdict(int, {insert: 1})
        for k, v in get_counts(a, insert, iterations - 1).items():
            counts[k] += v
        for k, v in get_counts(insert, b, iterations - 1).items():
            counts[k] += v
        cache[(a, b, iterations)] = counts
        return counts

    polymer = input_polymer
    counts = defaultdict(int, Counter(polymer))
    iterations = 40
    for a, b in zip(polymer[:-1], polymer[1:]):
        for k, v in get_counts(a, b, iterations).items():
            counts[k] += v
    counts = counts.values()
    print(f"Part 2: {max(counts)-min(counts)}\n")


solve(sample_input)
solve(actual_input)
