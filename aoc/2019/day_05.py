import os
from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]

computer = IntCodeComputer(program)
print(f"Part 1: {computer.run_program([1])}")

computer = IntCodeComputer(program)
print(f"Part 2: {computer.run_program([5])}")
