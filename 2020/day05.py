import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

occupied = set()
for line in lines:
    occupied.add(int(line.translate(str.maketrans("FBLR", "0101")), 2))

print(f"Part 1: {max(occupied)}")
for i in range(min(occupied), max(occupied)):
    if i not in occupied:
        print(f"Part 2: {i}")
