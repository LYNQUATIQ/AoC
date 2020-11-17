import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [int(line.rstrip("\n")) for line in open(input_file)]

fuel = 0
for x in lines:
    fuel += x // 3 - 2
print(f"Part 1: {fuel}")

fuel = 0
for x in lines:
    f = x // 3 - 2
    x = f
    while x > 0:
        x = max(x // 3 - 2, 0)
        f += x
    fuel += f

print(f"Part 2: {fuel}")
