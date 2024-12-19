"""https://adventofcode.com/2024/day/19"""

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
    patterns = patterns_input.split(", ")
    designs = designs_input.splitlines()

    def ways_to_design(design: str) -> int:
        if not design:
            return 1
        if design in ways_to_make_design:
            return ways_to_make_design[design]
        ways_to_make_design[design] = 0
        for start in [p for p in ways_to_make_pattern if design.startswith(p)]:
            ways_to_make_design[design] += ways_to_design(design[len(start) :])
        return ways_to_make_design[design]

    # Cache to store designs and the number of ways to make them
    ways_to_make_design: dict[str, int] = {}

    # Initialise ways_to_make_pattern with the known patterns (one way to make each)
    # and then add all the possible ways to build known patterns from others
    ways_to_make_pattern: dict[str, int] = {pattern: 1 for pattern in patterns}
    for pattern in patterns:
        ways_to_make_pattern[pattern] = ways_to_design(pattern)

    print(f"Part 1: {sum([(ways_to_design(design)>0) for design in designs])}")
    print(f"Part 2: {sum([ways_to_design(design) for design in designs])}\n")


solve(example_input)
solve(actual_input)
