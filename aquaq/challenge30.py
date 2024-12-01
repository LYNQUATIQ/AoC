import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

# lines = ["11010", "110", "00101011010"]

valid_starts = 0
for line in lines:
    ones = [i for i, x in enumerate(line) if x == "1"]
    for i in ones:
        is_valid = True
        if i > 0:
            is_valid = is_valid and not line[:i].count("1") % 2
        if i < len(line) - 1:
            is_valid = is_valid and not line[i + 1 :].count("1") % 2
        if is_valid:
            valid_starts += 1

print(valid_starts)
