import os
from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]

computer = IntCodeComputer(program, {1: 12, 2: 2})
computer.run_program()
print(f"Part 1: {computer.memory[0]}")

for noun in range(0, 100):
    for verb in range(0, 100):

        computer = IntCodeComputer(program, {1: noun, 2: verb})
        computer.run_program()
        if computer.memory[0] == 19690720:
            print(f"Part 2: {noun:02}{verb:02}")
            break
