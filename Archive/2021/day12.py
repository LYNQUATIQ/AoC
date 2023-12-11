"""https://adventofcode.com/2021/day/12"""
import os
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day12_input.txt")) as f:
    actual_input = f.read()


sample_input = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


def find_paths(edges, allow_double_visit: bool = False):
    number_of_paths = 0
    to_explore = [(("start",), allow_double_visit)]
    while to_explore:
        current_path, allow_double = to_explore.pop()
        for next_step in edges[current_path[-1]]:
            if next_step == "end":
                number_of_paths += 1
                continue
            if next_step.islower() and next_step in current_path:
                if allow_double:
                    to_explore.append(((*current_path, next_step), False))
                continue
            to_explore.append(((*current_path, next_step), allow_double))
    return number_of_paths


def solve(inputs):
    edges = defaultdict(set)
    for line in inputs.splitlines():
        a, b = line.split("-")
        if a != "end" and b != "start":
            edges[a].add(b)
        if b != "end" and a != "start":
            edges[b].add(a)

    print(f"Part 1: {find_paths(edges)}")
    print(f"Part 2: {find_paths(edges, True)}\n")


solve(sample_input)
solve(actual_input)
