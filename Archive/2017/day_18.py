import logging
import os
import string

from collections import defaultdict, deque

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_18.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_18_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


class Program:

    RUNNING = "Running"
    NOT_STARTED = "Not Started"
    WAITING = "Waiting"
    TERMINATED = "Terminated"

    def __init__(self, lines, p_register=0):
        self.program = []
        for line in lines:
            tokens = line.split(" ")
            instruction = tokens[0]
            params = tokens[1:]
            self.program.append((instruction, params))

        self.registers = defaultdict(int)
        self.registers["p"] = p_register
        self.send_queue = deque([])
        self.send_counter = 0
        self.pointer = 0
        self.status = self.NOT_STARTED

    def is_terminated(self):
        return self.status == self.TERMINATED

    def is_waiting(self):
        return self.status == self.WAITING

    def run_program(self, receive_queue):
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

            if instruction == "jgz":
                if get_value(params[0]) > 0:
                    self.pointer += get_value(params[1])
                    continue
            elif instruction == "set":
                self.registers[params[0]] = get_value(params[1])
            elif instruction == "add":
                self.registers[params[0]] += get_value(params[1])
            elif instruction == "mul":
                self.registers[params[0]] *= get_value(params[1])
            elif instruction == "mod":
                self.registers[params[0]] %= get_value(params[1])
            elif instruction == "snd":
                self.send_queue.append(get_value(params[0]))
                self.send_counter += 1
            elif instruction == "rcv":
                try:
                    self.registers[params[0]] = receive_queue.popleft()
                except IndexError:
                    self.status = self.WAITING
                    break
            self.pointer += 1

        return self.status


program = Program(lines)
program.run_program(deque([]))
print(f"Part 1: {program.send_queue[-1]}")

program0 = Program(lines, 0)
program1 = Program(lines, 1)
while True:
    program0.run_program(program1.send_queue)
    program1.run_program(program0.send_queue)
    if program0.is_terminated() or program1.is_terminated() or not program1.send_queue:
        break
print(f"Part 2: {program1.send_counter}")
