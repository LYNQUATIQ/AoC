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
        gates[wire] = (op, {a, b})

    while any(wires.get(w) is None for w in gates):
        for wire, (op, (a, b)) in gates.items():
            if a in wires and b in wires:
                wires[wire] = LOGICAL_OPERATORS[op](wires[a], wires[b])

    bit_count = max(int(w[1:]) for w in wires if w.startswith("z"))
    output = sum(wires[f"z{bit:02}"] * (2**bit) for bit in range(bit_count + 1))
    print(f"\nPart 1: {output}")

    if not find_dodgy_wires:
        return

    # To find the dodgy wires, try and find the gates that make up the half/full adders
    # for each bit - if any inputs are 'unexpected' then add them to the patch set.
    # See: https://www.geeksforgeeks.org/binary-adder-with-logic-gates/
    patches = set()

    def find_gate(expected_inputs, logical_op, patches) -> str:
        for wire, (op, actual_inputs) in gates.items():
            if op != logical_op:
                continue
            if expected_inputs & actual_inputs:
                if actual_inputs != expected_inputs:
                    patches |= actual_inputs ^ expected_inputs
                return wire

    # Check the two gates in the initial half adder at bit 0
    _ = find_gate({"x00", "y00"}, "XOR", patches)  # i.e. z00
    carry_in = find_gate({"x00", "y00"}, "AND", patches)

    # Check the five gates in each of the full adders for bits 1 onwards
    for bit in range(1, bit_count):
        x_nn, y_nn = f"x{bit:02}", f"y{bit:02}"
        partial_sum_xy = find_gate({x_nn, y_nn}, "XOR", patches)
        partial_carry_1 = find_gate({x_nn, y_nn}, "AND", patches)
        partial_carry_2 = find_gate({carry_in, partial_sum_xy}, "AND", patches)
        _ = find_gate({carry_in, partial_sum_xy}, "XOR", patches)  # i.e. z<nn>
        carry_in = find_gate({partial_carry_2, partial_carry_1}, "OR", patches)

    print(f"Part 2: {','.join(sorted(patches))}\n")


solve(example_input)
solve(actual_input, find_dodgy_wires=True)
