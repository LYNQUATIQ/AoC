import logging
import os
import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_23.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_23_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Program:

    RUNNING = "Running"
    NOT_STARTED = "Not Started"
    TERMINATED = "Terminated"

    def __init__(self, lines):
        self.program = []
        for line in lines:
            tokens = line.split(" ")
            instruction = tokens[0]
            params = tokens[1:]
            self.program.append((instruction, params))

        self.registers = defaultdict(int)
        self.pointer = 0
        self.mul_calls = 0
        self.status = self.NOT_STARTED

    def run_program(self):
        def get_value(param):
            if param in string.ascii_lowercase:
                return self.registers[param]
            else:
                return int(param)

        self.status = self.RUNNING
        while self.status == self.RUNNING:
            try:
                instruction, params = self.program[self.pointer]
            except IndexError:
                self.status = self.TERMINATED
                break

            if instruction == "jnz":
                if get_value(params[0]) != 0:
                    self.pointer += get_value(params[1])
                    continue
            elif instruction == "set":
                self.registers[params[0]] = get_value(params[1])
            elif instruction == "sub":
                self.registers[params[0]] -= get_value(params[1])
            elif instruction == "mul":
                self.mul_calls += 1
                self.registers[params[0]] *= get_value(params[1])

            self.pointer += 1

        return self.status


program = Program(lines)
program.run_program()
print(f"Part 1: {program.mul_calls}")


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True


b = 108400
h = 0
while b <= 125400:
    if not is_prime(b):
        h += 1
    b += 17

print(f"Part 2: {h}")
