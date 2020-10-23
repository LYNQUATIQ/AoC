import logging
import os
import re

from collections import defaultdict

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/2018_day_16.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_16_input - pt1.txt")
lines = [line.rstrip("\n") for line in open(file_path)]

file_path = os.path.join(script_dir, "inputs/day_16_input - pt2.txt")
program = [line.rstrip("\n") for line in open(file_path)]


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


test_lines = [t for t in chunker(lines, 4)]


def addr(params, registers):
    registers[params[3]] = registers[params[1]] + registers[params[2]]
    return registers


def addi(params, registers):
    registers[params[3]] = registers[params[1]] + params[2]
    return registers


def mulr(params, registers):
    registers[params[3]] = registers[params[1]] * registers[params[2]]
    return registers


def muli(params, registers):
    registers[params[3]] = registers[params[1]] * params[2]
    return registers


def banr(params, registers):
    registers[params[3]] = registers[params[1]] & registers[params[2]]
    return registers


def bani(params, registers):
    registers[params[3]] = registers[params[1]] & params[2]
    return registers


def borr(params, registers):
    registers[params[3]] = registers[params[1]] | registers[params[2]]
    return registers


def bori(params, registers):
    registers[params[3]] = registers[params[1]] | params[2]
    return registers


def setr(params, registers):
    registers[params[3]] = registers[params[1]]
    return registers


def seti(params, registers):
    registers[params[3]] = params[1]
    return registers


def gtir(params, registers):
    registers[params[3]] = int(params[1] > registers[params[2]])
    return registers


def gtri(params, registers):
    registers[params[3]] = int(registers[params[1]] > params[2])
    return registers


def gtrr(params, registers):
    registers[params[3]] = int(registers[params[1]] > registers[params[2]])
    return registers


def eqir(params, registers):
    registers[params[3]] = int(params[1] == registers[params[2]])
    return registers


def eqri(params, registers):
    registers[params[3]] = int(registers[params[1]] == params[2])
    return registers


def eqrr(params, registers):
    registers[params[3]] = int(registers[params[1]] == registers[params[2]])
    return registers


confirmed_codes = {
    "eqir": 0,
    "addi": 1,
    "gtir": 2,
    "setr": 3,
    "mulr": 4,
    "seti": 5,
    "muli": 6,
    "eqri": 7,
    "bori": 8,
    "bani": 9,
    "gtrr": 10,
    "eqrr": 11,
    "addr": 12,
    "gtri": 13,
    "borr": 14,
    "banr": 15,
}
instructions = {
    12: addr,
    1: addi,
    4: mulr,
    6: muli,
    15: banr,
    9: bani,
    14: borr,
    8: bori,
    3: setr,
    5: seti,
    2: gtir,
    13: gtri,
    10: gtrr,
    0: eqir,
    7: eqri,
    11: eqrr,
}


class Test:
    def __init__(self, before, values, after):
        self.before = [int(i) for i in before[9:-1].split(",")]
        self.values = [int(v) for v in values.split(" ")]
        self.after = [int(i) for i in after[9:-1].split(",")]

    def op_code(self):
        return self.values[0]

    def function_passes(self, function):
        _, a, b, c = self.values
        params = (_, a, b, c)
        before = self.before[:]
        after = function(params, before)
        return after == self.after


tests = set()
for test in test_lines:
    before, values, after, _ = test
    tests.add(Test(before, values, after))

registers = [0, 0, 0, 0]
for line in program:
    params = [int(i) for i in line.split(" ")]
    print(line, registers)
    instructions[params[0]](params, registers)

print(registers)
