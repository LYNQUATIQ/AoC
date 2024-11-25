import logging
import os

import string

from collections import defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Program:
    TERMINATED = "Terminated"
    RUNNING = "Running"
    NOT_STARTED = "Not Started"

    def __init__(self, lines):
        self.lines = lines
        self.registers = defaultdict(int)
        self.pointer = 0
        self.status = self.NOT_STARTED

    def set_registers(self, registers):
        for r, v in registers.items():
            self.registers[r] = v

    def run_program(self):

        def get_param_value(param):
            if param in string.ascii_letters:
                return self.registers[param]
            return int(param)

        self.status = self.RUNNING
        while self.status == self.RUNNING:

            try:
                tokens = self.lines[self.pointer].split(" ")
            except IndexError:
                self.status = self.TERMINATED
                continue

            if tokens[0] == "cpy":
                self.registers[tokens[2]] = get_param_value(tokens[1])
            elif tokens[0] == "inc":
                self.registers[tokens[1]] += 1
            elif tokens[0] == "dec":
                self.registers[tokens[1]] -= 1
            elif tokens[0] == "jnz":
                if get_param_value(tokens[1]) != 0:
                    self.pointer += get_param_value(tokens[2])
                    continue
            self.pointer += 1


p = Program(lines)
p.run_program()
print(f"Part 1: {p.registers['a']}")

p = Program(lines)
p.set_registers({"c": 1})
p.run_program()
print(f"Part 2: {p.registers['a']}")
