import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day05_input.txt")) as f:
    actual_input = f.read()

sample_input = """FBFBBFFRLR"""


def solve(inputs):
    occupied = set()
    for line in inputs.split("\n"):
        occupied.add(int(line.translate(str.maketrans("FBLR", "0101")), 2))

    print(f"Part 1: {max(occupied)}")
    for i in range(min(occupied), max(occupied)):
        if i not in occupied:
            print(f"Part 2: {i}")
    print()


solve(sample_input)
solve(actual_input)
