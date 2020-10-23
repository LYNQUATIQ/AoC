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

total_area = 0
ribbon = 0
for line in lines:
    d = sorted([int(i) for i in line.split("x")])
    total_area += 3 * d[0] * d[1] + 2 * d[1] * d[2] + 2 * d[0] * d[2]
    ribbon += 2 * d[0] + 2 * d[1] + d[0] * d[1] * d[2]

print(f"Part 1: {total_area}")
print(f"Part 2: {ribbon}")
