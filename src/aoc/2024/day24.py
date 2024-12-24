"""https://adventofcode.com/2024/day/24"""

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
        a, op, b, _, wire = line.split(" ")
        gates[wire] = (op, frozenset((a, b)))

    while any(wires.get(w) is None for w in gates):
        for wire, (op, inputs) in gates.items():
            a, b = inputs
            if a in wires and b in wires:
                wires[wire] = LOGICAL_OPERATORS[op](wires[a], wires[b])

    z_bits = {int(w[1:]) for w in wires if w.startswith("z")}
    value = 0
    for bit in range(max(z_bits) + 1):
        value += wires[f"z{bit:02}"] * (2**bit)
    print(f"\nPart 1: {value}")

    if not find_dodgy_wires:
        return

    # To find the dodgy wires, try and find the 5 gates that make up a 'full adder' for
    # each bit - if any of the inputs are 'unexpected' then add them to the patch list.
    # See: https://www.geeksforgeeks.org/binary-adder-with-logic-gates/
    bit_count, patches = max(z_bits), set()

    def find_gate(expected_inputs, logical_op, patches) -> str:
        for wire, (op, actual_inputs) in gates.items():
            if op != logical_op:
                continue
            if expected_inputs & actual_inputs:
                if actual_inputs != expected_inputs:
                    patches |= actual_inputs ^ expected_inputs
                return wire

    carry_in = find_gate({"x00", "y00"}, "AND", patches)
    for bit in range(1, bit_count):
        x, y = f"x{bit:02}", f"y{bit:02}"
        x_xor_y = find_gate({x, y}, "XOR", patches)
        x_and_y = find_gate({x, y}, "AND", patches)
        _ = find_gate({carry_in, x_xor_y}, "XOR", patches)
        next_carry = find_gate({carry_in, x_xor_y}, "AND", patches)
        carry_in = find_gate({next_carry, x_and_y}, "OR", patches)

    print(f"Part 2: {','.join(sorted(patches))}\n")


solve(example_input)
solve(actual_input, find_dodgy_wires=True)
