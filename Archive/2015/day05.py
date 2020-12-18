import os
import re


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()


def solve(inputs):
    words = inputs.splitlines()

    part1 = sum(
        bool(
            len([c for c in word if c in "aeiou"]) > 2
            and re.search(r"([a-z])\1", word)
            and not any(cc in word for cc in ["ab", "cd", "pq", "xy"])
        )
        for word in words
    )
    print(f"Part 1: {part1}")

    part2 = sum(
        bool(re.search(r"([a-z]{2}).*\1", word) and re.search(r"([a-z]).\1", word))
        for word in words
    )
    print(f"Part 2: {part2}")


solve(actual_input)
