import logging
import os

import string

from collections import defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Program:
    TERMINATED = "Terminated"
    RUNNING = "Running"
    NOT_STARTED = "Not Started"

    def __init__(self, lines):
        self.lines = [line.split(" ") for line in lines]
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

        last_output = True
        self.status = self.RUNNING
        while self.status == self.RUNNING:

            try:
                tokens = self.lines[self.pointer]
            except IndexError:
                self.status = self.TERMINATED
                continue

            logging.debug(
                f"{self.pointer:2}: regs[{', '.join([f'{k}:{v}' for k, v in self.registers.items()])}  {tokens}"
            )

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
            elif tokens[0] == "out":
                # assert get_param_value(tokens[1]) == not last_output
                # last_output = not last_output
                self.registers["X"] = get_param_value(tokens[1])
                print(self.registers["X"], self.registers["a"])
                input()

            self.pointer += 1


def recreate_program(a_reg):
    while True:
        a = 2538 + a_reg

        while True:
            b = a
            a = 0
            c = 2

            while True:
                if b == 0:
                    break
                else:
                    b -= 1
                    c -= 1  # c = 2 - b
                if c == 0:
                    a += 1
                    c = 2
            #  a = a // 2
            b = 2
            while True:
                if c == 0:
                    break
                else:
                    b -= 1  # b = 2 - c
                    c -= 1
            #  b = a % 2

            print(b)
            if a == 0:
                break


x = 1
while x <= 2538:
    if x % 2:
        x = x * 2
    else:
        x = x * 2 + 1

print(f"Part 1: {x - 2538}")
