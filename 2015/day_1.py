import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

floor = 0
basement_entry_i = None
for i, c in enumerate(lines[0], 1):
    if c == "(":
        floor += 1
    else:
        floor -= 1
    if basement_entry_i is None and floor == -1:
        basement_entry_i = i

print(f"Part 1: {floor}")
print(f"Part 2: {basement_entry_i}")
