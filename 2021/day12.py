import os

from collections import defaultdict

from utils import print_time_taken

with open(os.path.join(os.path.dirname(__file__), f"inputs/day12_input.txt")) as f:
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
    number_of_paths, path_allows_double = 0, defaultdict(lambda: allow_double_visit)
    to_explore = [("start",)]
    while to_explore:
        current_path = to_explore.pop()
        for next_step in edges[current_path[-1]]:
            if next_step == "end":
                number_of_paths += 1
                continue
            allow_double = path_allows_double[current_path]
            if next_step.islower() and next_step in current_path:
                if not allow_double:
                    continue
                allow_double = False
            to_explore.append((*current_path, next_step))
            path_allows_double[to_explore[-1]] = allow_double

    return number_of_paths


@print_time_taken
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
