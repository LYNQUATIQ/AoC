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

    ways_to_build_pattern = {pattern: 1 for pattern in patterns_input.split(", ")}
    designs = designs_input.splitlines()

    def possible_ways(design: str) -> int:
        if design in ways_to_build_pattern:
            return ways_to_build_pattern[design]
        new_ways = 0
        for pattern, ways in list(ways_to_build_pattern.items()):
            if design.startswith(pattern):
                new_ways += ways * possible_ways(design[len(pattern) :])
        ways_to_build_pattern[design] = new_ways
        return new_ways

    part_1 = sum([int(possible_ways(design) > 0) for design in designs])
    print(f"Part 1: {part_1}")
    part_2 = sum([possible_ways(design) for design in designs])
    print(f"Part 2: {part_2}\n")
    for design in designs:
        print(design, ways_to_build_pattern[design])


solve(example_input)
# solve(actual_input)
