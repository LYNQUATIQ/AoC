"""https://adventofcode.com/2024/day/17"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 17)
example_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

REG_A, REG_B, REG_C = "A", "B", "C"
ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = 0, 1, 2, 3, 4, 5, 6, 7


def combo_op(combo_operand: int, registers: dict[str, int]) -> int:
    return (
        combo_operand
        if combo_operand <= 3
        else registers[{4: REG_A, 5: REG_B, 6: REG_C}[combo_operand]]
    )


def run_program(program: list[int], register_a: int) -> list[int]:
    """Run the program and return the output using the following opcodes:
    adv/bdv/cdv - operations that take right hand bits from A and put them into A/B/C
    bxl/bxc     - operations that flip bits in B using XOR
    bst/out     - operations that puts the last 3 bits of something into B or output
    jnz         - operation that controls the program flow (jumps if A!=0)
    """
    registers = {REG_A: register_a, REG_B: 0, REG_C: 0}
    pointer, output = 0, []
    while pointer < len(program):
        opcode, operand = program[pointer], program[pointer + 1]
        pointer += 2
        if opcode == ADV:
            registers[REG_A] = registers[REG_A] // (2 ** combo_op(operand, registers))
        elif opcode == BDV:
            registers[REG_B] = registers[REG_A] // (2 ** combo_op(operand, registers))
        elif opcode == CDV:
            registers[REG_C] = registers[REG_A] // (2 ** combo_op(operand, registers))
        elif opcode == BXL:
            registers[REG_B] = registers[REG_B] ^ operand
        elif opcode == BXC:
            registers[REG_B] = registers[REG_B] ^ registers[REG_C]
        elif opcode == BST:
            registers[REG_B] = combo_op(operand, registers) % 8
        elif opcode == OUT:
            output.append(combo_op(operand, registers) % 8)
        elif opcode == JNZ:
            pointer = pointer if registers[REG_A] == 0 else operand
    return output


def reverse_engineer(opcodes: list[int], register_a: int, loop: list[int]) -> int:
    if not opcodes:
        return register_a
    for next_3_bits in range(8):
        candidate_a = register_a * 8 + next_3_bits
        output_a = run_program(loop, candidate_a)[0]
        if output_a == opcodes[-1]:
            try:
                return reverse_engineer(opcodes[:-1], candidate_a, loop)
            except StopIteration:
                continue
    raise StopIteration


def solve(inputs: str):
    registers_input, program_input = inputs.split("\n\n")
    program = list(map(int, program_input[8:].split(",")))
    register_a = int(registers_input.splitlines()[0][12:])

    print(f"Part 1: {','.join(map(str, run_program(program, register_a)))}")

    assert program[-2:] == [3, 0]
    loop = program[:-2]
    register_a = reverse_engineer(program, 0, loop)
    assert run_program(program, register_a) == program
    print(f"Part 2: {register_a}\n")


solve(example_input)
solve(actual_input)
