import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day08_input.txt")) as f:
    actual_input = f.read()

sample_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


class HandheldComputer:
    INITIALISED = "Initialised"
    RUNNING = "Running"
    LOOP_ERROR = "Loop Error"
    TERMINATED = "Terminated"

    def __init__(self, program, patches={}):
        self.program = program
        self.patches = patches
        self.stack_trace = {}
        self.pointer = 0
        self.accumulator = 0
        self.status = self.INITIALISED

    def run_program(self):
        self.status = self.RUNNING
        while True:
            if self.pointer in self.stack_trace:
                return self.LOOP_ERROR
            if self.pointer not in self.program:
                return self.TERMINATED
            instruction, param = self.program[self.pointer]
            instruction = self.patches.get(self.pointer, instruction)
            self.stack_trace[self.pointer] = (instruction, param, self.accumulator)
            getattr(self, instruction)(param)

    def acc(self, param):
        self.accumulator += param
        self.pointer += 1

    def jmp(self, param):
        self.pointer += param

    def nop(self, param):
        self.pointer += 1


def solve(inputs):
    program = {}
    for i, line in enumerate(inputs.splitlines()):
        instruction, param = line.split()
        program[i] = (instruction, int(param))

    computer = HandheldComputer(program)
    computer.run_program()
    print(f"Part 1: {computer.accumulator}")

    stack_trace = computer.stack_trace
    for pointer, (instruction, _, _) in stack_trace.items():
        if instruction == "acc":
            continue
        patch = {pointer: {"nop": "jmp", "jmp": "nop"}[instruction]}
        computer = HandheldComputer(program, patches=patch)
        if computer.run_program() == HandheldComputer.TERMINATED:
            break
    print(f"Part 2: {computer.accumulator}\n")


solve(sample_input)
solve(actual_input)
