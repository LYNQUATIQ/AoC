"""https://adventofcode.com/2024/day/24
   https://www.geeksforgeeks.org/binary-adder-with-logic-gates/
"""

from collections import defaultdict

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


def solve(inputs: str, find_dodgy_wires=False):
    wire_inputs, gate_inputs = inputs.split("\n\n")
    wires = {}
    for line in wire_inputs.splitlines():
        wire, value = line.split(": ")
        wires[wire] = bool(int(value))

    gates = {}
    for line in gate_inputs.splitlines():
        a, op, b, _, gate_wire = line.split(" ")
        gates[gate_wire] = (op, frozenset((a, b)))

    def decimal_value(prefix: str):
        value = 0
        for i, wire in enumerate(sorted({w for w in wires if w.startswith(prefix)})):
            value += wires[wire] * (2**i)
        return value

    while any(wires.get(w) is None for w in gates):
        for gate_wire, (op, inputs) in gates.items():
            a, b = inputs
            if a in wires and b in wires:
                wires[gate_wire] = LOGICAL_OPERATORS[op](wires[a], wires[b])

    print(f"Part 1: {decimal_value('z')}")
    if not find_dodgy_wires:
        print()
        return

    patches = set()

    def find_gate(input1, input2, logical_op, patches) -> str:
        for gate_wire, (op, inputs) in gates.items():
            if op != logical_op:
                continue
            if input1 in inputs or input2 in inputs:
                if inputs != frozenset((input1, input2)):
                    # Gonna need a patch
                    if input1 in inputs:
                        patches |= {input2} | (inputs - {input1})
                    else:
                        patches |= {input1} | (inputs - {input2})
                return gate_wire

        raise ValueError(f"Could not find {logical_op} gate for {input1} and {input2}")

    half_adder_and, half_adder_xor = {}, {}
    for gate_wire, (op, inputs) in gates.items():
        a, b = sorted(inputs)
        if a.startswith("x") and b.startswith("y"):
            assert a[1:] == b[1:] and op in ("AND", "XOR")
            bit_number = int(a[1:])
            if op == "AND":
                half_adder_and[bit_number] = gate_wire
            elif op == "XOR":
                half_adder_xor[bit_number] = gate_wire
                if bit_number == 0:
                    assert gate_wire == f"z{bit_number:02}"

    bit_count = max(half_adder_xor) + 1
    full_adder_or = {0: half_adder_and[0]}
    for bit in range(1, bit_count):
        c_in = full_adder_or[bit - 1]
        find_gate(c_in, half_adder_xor[bit], "XOR", patches)
        c_out = find_gate(c_in, half_adder_xor[bit], "AND", patches)
        full_adder_or[bit] = find_gate(c_out, half_adder_and[bit], "OR", patches)

    print(f"Part 2: {','.join(sorted(patches))}\n")


solve(example_input)
solve(actual_input, find_dodgy_wires=True)
