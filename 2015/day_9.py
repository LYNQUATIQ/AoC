import logging
import os
import sys

from itertools import permutations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

to_visit = set()
distances = {}

for line in lines:
    tokens = line.split(" ")
    a, b, distance = tokens[0], tokens[2], int(tokens[4])
    to_visit.add(a)
    to_visit.add(b)
    distances[(a, b)] = distance
    distances[(b, a)] = distance

cities = list(to_visit)

shortest_distance = sys.maxsize
longest_distance = 0
for route in permutations(cities):
    distance = 0
    a = route[0]
    for b in route[1:]:
        distance += distances[(a, b)]
        a = b
    shortest_distance = min(shortest_distance, distance)
    longest_distance = max(longest_distance, distance)

print(f"Part 1: {shortest_distance}")
print(f"Part 2: {longest_distance}")

