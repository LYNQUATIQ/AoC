import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()


def solve(inputs):
    occupied = set()
    for line in inputs.split("\n"):
        occupied.add(int(line.translate(str.maketrans("FBLR", "0101")), 2))

    print(f"Part 1: {max(occupied)}")
    for i in range(min(occupied), max(occupied)):
        if i not in occupied:
            print(f"Part 2: {i}\n")


solve(actual_input)
