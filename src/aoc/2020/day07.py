import os
import re

from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "inputs/day07_input.txt")) as f:
    actual_input = f.read()

example_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


def solve(inputs):
    inner_bags = defaultdict(list)
    outer_bags = defaultdict(set)
    for line in inputs.split("\n"):
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
    print(f"Part 2: {inner_bag_count(MY_BAG)}\n")


solve(example_input)
solve(actual_input)
