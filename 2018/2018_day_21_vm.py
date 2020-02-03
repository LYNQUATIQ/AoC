import logging
import os
import re

from collections import defaultdict

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_21.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_21_input.txt")
program = [line.rstrip("\n") for line in open(file_path)]


class DeviceVM:
    def addr(self, params, registers):
        registers[params[2]] = registers[params[0]] + registers[params[1]]
        return registers

    def addi(self, params, registers):
        registers[params[2]] = registers[params[0]] + params[1]
        return registers

    def mulr(self, params, registers):
        registers[params[2]] = registers[params[0]] * registers[params[1]]
        return registers

    def muli(self, params, registers):
        registers[params[2]] = registers[params[0]] * params[1]
        return registers

    def banr(self, params, registers):
        registers[params[2]] = registers[params[0]] & registers[params[1]]
        return registers

    def bani(self, params, registers):
        registers[params[2]] = registers[params[0]] & params[1]
        return registers

    def borr(self, params, registers):
        registers[params[2]] = registers[params[0]] | registers[params[1]]
        return registers

    def bori(self, params, registers):
        registers[params[2]] = registers[params[0]] | params[1]
        return registers

    def setr(self, params, registers):
        registers[params[2]] = registers[params[0]]
        return registers

    def seti(self, params, registers):
        registers[params[2]] = params[0]
        return registers

    def gtir(self, params, registers):
        registers[params[2]] = int(params[0] > registers[params[1]])
        return registers

    def gtri(self, params, registers):
        registers[params[2]] = int(registers[params[0]] > params[1])
        return registers

    def gtrr(self, params, registers):
        registers[params[2]] = int(registers[params[0]] > registers[params[1]])
        return registers

    def eqir(self, params, registers):
        registers[params[2]] = int(self, params[0] == registers[params[1]])
        return registers

    def eqri(self, params, registers):
        registers[params[2]] = int(registers[params[0]] == params[1])
        return registers

    def eqrr(self, params, registers):
        registers[params[2]] = int(registers[params[0]] == registers[params[1]])
        return registers

    instructions = {
        0: eqir,
        1: addi,
        2: gtir,
        3: setr,
        4: mulr,
        5: seti,
        6: muli,
        7: eqri,
        8: bori,
        9: bani,
        10: gtrr,
        11: eqrr,
        12: addr,
        13: gtri,
        14: borr,
        15: banr,
    }

    registers = [0, 0, 0, 0, 0, 0]
    instructions = {}
    ip_register = None

    def __init__(self, program):
        for i, line in enumerate(program):
            if line[0:3] == "#ip":
                self.ip_register = int(line[4:5])
                print(f"IP register set to: {self.ip_register}")
                continue
            self.instructions[i - 1] = (
                line[0:4],
                [int(i) for i in line[5:].split(" ")],
            )
        for i, instr in self.instructions.items():
            print(i, instr)

    def run_program(self):
        pointer = 0
        while True:
            try:
                operation, params = self.instructions[pointer]
            except KeyError:
                break

            if self.ip_register is not None:
                self.registers[self.ip_register] = pointer
            self.registers = getattr(self, operation)(params, self.registers)
            try:
                debug_message, do_input = {
                    7: (
                        f"Starting outer loop - r2={self.registers[2]:#x}  r3={self.registers[3]:#x}",
                        True,
                    ),
                    8: (
                        f"    Starting inner loop - r2={self.registers[2]:#x}  r3={self.registers[3]:#x}",
                        False,
                    ),
                    12: (f"    r3 now {self.registers[3]:#x}", True),
                    23: (
                        f"    r2 changing from {self.registers[2]:#x} to {self.registers[1]:#x}",
                        False,
                    ),
                }[pointer]
                print(debug_message)
                logging.debug(debug_message)

            except KeyError:
                pass
            logging.debug(f"{pointer} - {operation} {params} >> {self.registers}")
            if self.ip_register is not None:
                pointer = self.registers[self.ip_register]
            pointer += 1


vm = DeviceVM(program)
vm.run_program()
