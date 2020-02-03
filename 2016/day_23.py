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

        tgl_map = {"inc": "dec", "dec": "inc", "tgl": "inc", "jnz": "cpy", "cpy": "jnz"}

        def get_param_value(param):
            if param in string.ascii_letters:
                return self.registers[param]
            return int(param)

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
                try:
                    self.registers[tokens[2]] = get_param_value(tokens[1])
                except KeyError:
                    pass
            elif tokens[0] == "inc":
                self.registers[tokens[1]] += 1
            elif tokens[0] == "dec":
                self.registers[tokens[1]] -= 1
            elif tokens[0] == "jnz":
                if get_param_value(tokens[1]) != 0:
                    self.pointer += get_param_value(tokens[2])
                    continue
            elif tokens[0] == "tgl":
                x = self.pointer + get_param_value(tokens[1])
                try:
                    self.lines[x][0] = tgl_map[self.lines[x][0]]
                except IndexError:
                    pass

            self.pointer += 1


p = Program(lines)
p.set_registers({"a": 7})
p.run_program()
print(f"Part 1: {p.registers['a']}")


def recreate_program(a_reg):
    a = a_reg
    for f in range(1, a_reg):
        a *= f
    a += 71 * 75
    return a


print(f"Part 2: {recreate_program(12)}")
