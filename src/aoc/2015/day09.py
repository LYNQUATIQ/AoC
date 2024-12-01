import os
import math

from itertools import permutations

with open(os.path.join(os.path.dirname(__file__), "inputs/day09_input.txt")) as f:
    actual_input = f.read()


def solve(inputs):
    lines = map(lambda x: x.split(), inputs.splitlines())

    to_visit, distances = set(), {}

    for a, b, distance in map(lambda x: (x[0], x[2], int(x[4])), lines):
        to_visit.add(a)
        to_visit.add(b)
        distances[(a, b)] = distance
        distances[(b, a)] = distance

    shortest_distance, longest_distance = math.inf, 0
    for route in permutations(to_visit):
        distance = 0
        a = route[0]
        for b in route[1:]:
            distance += distances[(a, b)]
            a = b
        shortest_distance = min(shortest_distance, distance)
        longest_distance = max(longest_distance, distance)

    print(f"Part 1: {shortest_distance}")
    print(f"Part 2: {longest_distance}\n")


solve(actual_input)
