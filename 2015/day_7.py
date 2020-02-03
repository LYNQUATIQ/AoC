import logging
import os

import re

from collections import defaultdict

from grid_system import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

regex = re.compile(
    r"^(?P<instruction>(toggle)|(turn on)|(turn off)) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)$"
)


class Wire:
    def __init__(self, identifier, inputs=[], gate=None):
        self.identifier = identifier
        self.inputs = inputs
        self.gate = gate
        self._output = None

    def __repr__(self):
        return f"{self.identifier} - {self.gate} {self.inputs}"

    def output(self, network):
        if self._output is not None:
            return self._output

        def input_value(x):
            try:
                return int(x)
            except ValueError:
                return network.output(x)

        input1 = input_value(self.inputs[0])
        try:
            input2 = input_value(self.inputs[1])
        except IndexError:
            pass

        if self.gate == "VALUE":
            self._output = input1
        elif self.gate == "NOT":
            self._output = input1 ^ 65535
        elif self.gate == "LSHIFT":
            self._output = input1 << input2
        elif self.gate == "RSHIFT":
            self._output = input1 >> input2
        elif self.gate == "AND":
            self._output = input1 & input2
        elif self.gate == "OR":
            self._output = input1 | input2
        else:
            raise NotImplementedError

        return self._output


class Network:
    def __init__(self, lines):
        self.wires = {}
        for line in lines:
            tokens = line.split(" -> ")
            identifier = tokens[1]
            tokens = tokens[0].split(" ")

            if len(tokens) == 1:
                inputs = [tokens[0]]
                gate = "VALUE"
            elif len(tokens) == 2:
                gate = tokens[0]
                inputs = [tokens[1]]
            else:
                gate = tokens[1]
                inputs = [tokens[0], tokens[2]]

            wire = Wire(identifier, inputs, gate)
            self.wires[identifier] = wire

    def output(self, identifier):
        return self.wires[identifier].output(self)


network = Network(lines)
wire_a = network.output("a")
print(f"Part 1: {wire_a}")

network = Network(lines)
network.wires["b"].gate = "VALUE"
network.wires["b"].inputs = [wire_a]
print(f"Part 2: {network.output('a')}")
