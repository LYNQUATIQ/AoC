import os
import re
from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

inner_bags = defaultdict(list)
outer_bags = defaultdict(set)
for line in lines:
    outer_bag = re.match(r"^(\D+) bags", line).groups()[0]
    for n, inner_bag in re.findall(r"(\d+) (\D+) bag[s]?[,|\.]", line):
        inner_bags[outer_bag].append((inner_bag, int(n)))
        outer_bags[inner_bag].add(outer_bag)


def get_outer_bags(bag):
    bags_to_search = set([bag])
    results = set()
    while bags_to_search:
        bag = bags_to_search.pop()
        for outer_bag in outer_bags[bag]:
            results.add(outer_bag)
            bags_to_search.add(outer_bag)
    return results


def inner_bag_count(bag):
    return sum(n + n * inner_bag_count(b) for b, n in inner_bags[bag])


MY_BAG = "shiny gold"
print(f"Part 1: {len(get_outer_bags(MY_BAG))}")
print(f"Part 2: {inner_bag_count(MY_BAG)}")
