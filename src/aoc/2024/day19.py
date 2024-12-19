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

ways_to_make_design: dict[str, set[str]] = {}


def possible_ways(design: str, ignore_this: bool = False) -> set[str]:
    if design in ways_to_make_design and not ignore_this:
        return ways_to_make_design[design]

    new_ways = set()
    starts = [
        (p, w) for p, w in ways_to_make_design.items() if design[:-1].startswith(p)
    ]
    for start, ways_to_start in starts:
        rest_of_design = design[len(start) :]
        ways_to_rest = possible_ways(rest_of_design)
        for way_to_start, rest_of_way in product(ways_to_start, ways_to_rest):
            new_ways.add(f"{way_to_start},{rest_of_way}")
    ways_to_make_design[design] = new_ways
    return new_ways


def solve(inputs: str):
    patterns_input, designs_input = inputs.split("\n\n")
    patterns = patterns_input.split(", ")
    designs = designs_input.splitlines()

    for pattern in patterns:
        ways_to_make_design[pattern] = {pattern}

    # Need to add all the possible ways to build known patterns from others
    for pattern in patterns:
        ways_to_make_design[pattern] |= possible_ways(pattern, ignore_this=True)

    # Now add all the possible ways to build the requested designs
    for design in designs:
        ways_to_make_design[design] = possible_ways(design)

    print(f"Part 1: {sum([bool(ways_to_make_design[design]) for design in designs])}")
    print(f"Part 2: {sum([len(ways_to_make_design[design]) for design in designs])}\n")


solve(example_input)
solve(actual_input)
