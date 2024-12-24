"""https://adventofcode.com/2024/day/24"""

from collections import defaultdict
from tkinter import W

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 24)


example_input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


LOGICAL_OPERATORS = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
}


def solve(inputs: str):
    wire_inputs, gate_inputs = inputs.split("\n\n")
    wires = {}
    for line in wire_inputs.splitlines():
        wire, value = line.split(": ")
        wires[wire] = bool(int(value))

    gates = {}
    z_wires = set()
    inputs_to = defaultdict(list)
    for line in gate_inputs.splitlines():
        a, op, b, _, output = line.split(" ")
        gates[output] = (op, (a, b))
        inputs_to[a].append(output)
        inputs_to[b].append(output)
        if output.startswith("z"):
            z_wires.add(output)

    while any(wires.get(z) is None for z in z_wires):
        for output, (op, (a, b)) in gates.items():
            if a in wires and b in wires:
                wires[output] = LOGICAL_OPERATORS[op](wires[a], wires[b])

    output_value = 0
    for i, z_wire in enumerate(sorted(z_wires)):
        output_value += wires[z_wire] * (2**i)

    print(f"Part 1: {output_value}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
