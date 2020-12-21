import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day07_input.txt")) as f:
    actual_input = f.read()


class Wire:
    LOGIC_GATES = {
        "VALUE": lambda a, _: a,
        "NOT": lambda a, _: a ^ 65535,
        "LSHIFT": lambda a, b: a << b,
        "RSHIFT": lambda a, b: a >> b,
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
    }

    def __init__(self, identifier, inputs=[], gate=None):
        self.identifier = identifier
        self.inputs = inputs
        self.gate = gate
        self._output = None

    def output(self, network):
        if self._output is not None:
            return self._output

        def input_value(x):
            try:
                return int(x)
            except ValueError:
                return network.output(x)

        input1, input2 = input_value(self.inputs[0]), None
        try:
            input2 = input_value(self.inputs[1])
        except IndexError:
            pass

        self._output = self.LOGIC_GATES[self.gate](input1, input2)
        return self._output


class Network:
    def __init__(self, inputs):
        self.wires = {}
        for line in inputs.splitlines():
            tokens, identifier = line.split(" -> ")
            tokens = tokens.split()
            if len(tokens) == 1:
                gate, inputs = "VALUE", [tokens[0]]
            elif len(tokens) == 2:
                gate, inputs = tokens[0], [tokens[1]]
            else:
                gate, inputs = tokens[1], [tokens[0], tokens[2]]
            self.wires[identifier] = Wire(identifier, inputs, gate)

    def output(self, identifier):
        return self.wires[identifier].output(self)


def solve(inputs):
    network = Network(inputs)
    wire_a = network.output("a")
    print(f"Part 1: {wire_a}")

    network = Network(inputs)
    network.wires["b"].gate = "VALUE"
    network.wires["b"].inputs = [wire_a]
    print(f"Part 2: {network.output('a')}\n")


solve(actual_input)
