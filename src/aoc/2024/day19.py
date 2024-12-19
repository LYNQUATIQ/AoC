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

    def is_possible(design: str, patterns_so_far: tuple[str] = ()) -> bool:
        # print(f"   Checking {design}  (so far: {patterns_so_far})")
        if design == "":
            return True
        for pattern in patterns:
            if design.startswith(pattern):
                if is_possible(design[len(pattern) :], (*patterns_so_far, pattern)):
                    return True
        return False

    number_possible = 0
    for design in designs:
        # print("Testing ", design)
        x = is_possible(design)
        # print("      ->", x)
        number_possible += int(x)

    print(f"Part 1: {number_possible}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
