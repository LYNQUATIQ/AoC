"""https://adventofcode.com/2023/day/8"""
import os
import math

from itertools import cycle

with open(os.path.join(os.path.dirname(__file__), "inputs/day08_input.txt")) as f:
    actual_input = f.read()


sample_input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

sample_input2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def parse_inputs(
    inputs: str, start: str, target: str
) -> tuple[str, dict[str, tuple[str, str]], set[str], set[str]]:
    route, node_data = inputs.split("\n\n")
    nodes = {line[0:3]: (line[7:10], line[12:15]) for line in node_data.splitlines()}
    starts = {n for n in nodes if n.endswith(start)}
    targets = {n for n in nodes if n.endswith(target)}
    return (route, nodes, starts, targets)


def traverse_nodes(
    nodes: dict[str, tuple[str, str]], route: str, start: str, targets: set[str]
) -> int:
    direction = cycle(route)
    steps, location = 0, start
    while location not in targets:
        steps += 1
        location = nodes[location][0 if next(direction) == "L" else 1]
    return steps


def solve(inputs, inputs2):
    route, nodes, _, targets = parse_inputs(inputs, "AAA", "ZZZ")
    steps = traverse_nodes(nodes, route, "AAA", targets)
    print(f"Part 1: {steps}")

    route, nodes, ghosts, targets = parse_inputs(inputs2, "A", "Z")
    steps = [traverse_nodes(nodes, route, ghost, targets) for ghost in ghosts]
    print(f"Part 2: {math.lcm(*steps)}\n")


solve(sample_input, sample_input2)
solve(actual_input, actual_input)
