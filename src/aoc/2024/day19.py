"""https://adventofcode.com/2024/day/19"""

from collections import defaultdict

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


def solve(inputs: str):
    patterns_input, designs_input = inputs.split("\n\n")

    ways_to_build_pattern = {
        pattern: [[pattern]] for pattern in patterns_input.split(", ")
    }
    designs = designs_input.splitlines()
    designs = ["brwr"]

    def possible_ways(design: str) -> list[list[str]]:
        if design in ways_to_build_pattern:
            return ways_to_build_pattern[design]
        new_ways = []
        for pattern, ways in list(ways_to_build_pattern.items()):
            if design.startswith(pattern):
                new_ways += [ways + w for w in possible_ways(design[len(pattern) :])]
        ways_to_build_pattern[design] = new_ways
        return new_ways

    part_1 = sum([int(len(possible_ways(design)) > 0) for design in designs])
    print(f"Part 1: {part_1}")
    part_2 = sum([len(possible_ways(design)) for design in designs])
    print(f"Part 2: {part_2}\n")
    for design in designs[:1]:
        ways = ways_to_build_pattern[design]
        print(ways)
        print(design, [",".join(way[0]) for way in ways])


solve(example_input)
# solve(actual_input)
