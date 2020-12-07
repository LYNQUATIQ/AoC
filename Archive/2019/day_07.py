import os
from itertools import permutations

from intcode_computer import IntCodeComputerNetwork

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]

NUM_COMPUTERS = 5


def run_network(inputs):
    computers = IntCodeComputerNetwork(program, NUM_COMPUTERS)
    computers.add_inputs({i: [p] for i, p in enumerate(inputs)})
    return computers.run_program(0)


part1 = max(run_network(perms) for perms in permutations(range(5)))
print(f"Part 1: {part1}")

part2 = max(run_network(perms) for perms in permutations(range(5, 10)))
print(f"Part 2: {part2}")
