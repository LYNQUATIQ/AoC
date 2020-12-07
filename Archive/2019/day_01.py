import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [int(line.rstrip("\n")) for line in open(input_file)]


print(f"Part 1: {sum(x // 3 - 2 for x in lines)}")

fuel = 0
for x in lines:
    f = x // 3 - 2
    x = f
    while x > 0:
        x = max(x // 3 - 2, 0)
        f += x
    fuel += f

print(f"Part 2: {fuel}")
