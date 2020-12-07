import os
import re
from collections import defaultdict, deque

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

inner_bags = defaultdict(dict)
outer_bags = defaultdict(list)
for line in lines:
    outer_bag = re.match(r"^(\D+) bags contain .+$", line).groups()[0]
    for n, inner_bag in re.findall(r"(\d+) (\D+) bag[s]?[,|\.]", line):
        inner_bags[outer_bag][inner_bag] = int(n)
        outer_bags[inner_bag].append(outer_bag)


def get_containers(bag):
    containers = set()
    bags_to_find = deque([bag])
    while bags_to_find:
        bag = bags_to_find.popleft()
        for outer_bag in outer_bags[bag]:
            if outer_bag not in containers:
                containers.add(outer_bag)
                bags_to_find.append(outer_bag)
    return containers


def inner_bag_count(bag):
    return sum(n + n * inner_bag_count(bag) for bag, n in inner_bags[bag].items())


MY_BAG = "shiny gold"
print(f"Part 1: {len(get_containers(MY_BAG))}")
print(f"Part 2: {inner_bag_count(MY_BAG)}")
