import os
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""


def solve(inputs):
    part1, part2 = 0, 0
    for line in inputs.split("\n"):
        a, b, c, p = re.match(r"^(\d+)-(\d+) ([a-z]): ([a-z]+)$", line).groups()
        a, b = int(a), int(b)
        part1 += a <= p.count(c) <= b
        part2 += (p[a - 1] == c) + (p[b - 1] == c) == 1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
