"""https://adventofcode.com/2024/day/19"""

from collections import defaultdict
from itertools import product

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 19)


example_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

ways_to_make_design: dict[str, int] = {}
ways_to_make_pattern: dict[str, int] = {}


def possible_ways(design: str, ignore_this: bool = False) -> int:
    if not design:
        return 1
    if design in ways_to_make_design and not ignore_this:
        return ways_to_make_design[design]
    ways = 0
    possible_starts = [p for p in ways_to_make_pattern if design.startswith(p)]
    for start in possible_starts:
        # ways += ways_to_make_design[start] * possible_ways(design[len(start) :])
        ways += possible_ways(design[len(start) :])
    if ways:
        ways_to_make_design[design] = ways
    return ways


def solve(inputs: str):
    patterns_input, designs_input = inputs.split("\n\n")
    patterns = patterns_input.split(", ")
    designs = designs_input.splitlines()

    for pattern in patterns:
        ways_to_make_pattern[pattern] = 1

    # Need to add all the possible ways to build known patterns from others
    for pattern in patterns:
        ways_to_make_pattern[pattern] = possible_ways(pattern, ignore_this=True)

    # Now add all the possible ways to build the requested designs
    for design in designs:
        ways_to_make_design[design] = possible_ways(design)

    print(f"Part 1: {sum([(ways_to_make_design[design]>0) for design in designs])}")
    print(f"Part 2: {sum([ways_to_make_design[design] for design in designs])}\n")


solve(example_input)
solve(actual_input)
# 41271664854551032 too high
