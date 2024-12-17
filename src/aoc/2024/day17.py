"""https://adventofcode.com/2024/day/17"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 17)
example_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def combo(operand, registers):
    if operand <= 3:
        return operand
    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    raise ValueError(f"Invalid combo operand {operand}")


def run_program(program: list[int], register_a: int) -> list[int]:
    registers = {"A": register_a, "B": 0, "C": 0}
    pointer, output = 0, []
    while pointer < len(program):
        opcode, operand = program[pointer], program[pointer + 1]
        pointer += 2
        if opcode == 0:  # adv
            registers["A"] //= 2 ** combo(operand, registers)
        elif opcode == 1:  # bxl
            registers["B"] ^= operand
        elif opcode == 2:  # bst
            registers["B"] = combo(operand, registers) % 8
        elif opcode == 3:  # jnz
            pointer = pointer if registers["A"] == 0 else operand
        elif opcode == 4:  # bxl
            registers["B"] ^= registers["C"]
        elif opcode == 5:  # out
            output.append(combo(operand, registers) % 8)
        elif opcode == 6:  # bdv
            registers["B"] = registers["A"] // (2 ** combo(operand, registers))
        elif opcode == 7:  # cdv
            registers["C"] = registers["A"] // (2 ** combo(operand, registers))
    return output


def reverse_engineer(
    opcodes: list[int], register_a_so_far: int, loop_section: list[int]
) -> int:
    if not opcodes:
        return register_a_so_far
    for next_3_bits in range(8):
        candidate_a = register_a_so_far * 8 + next_3_bits
        output_a = run_program(loop_section, candidate_a)[0]
        if output_a == opcodes[-1]:
            try:
                return reverse_engineer(opcodes[:-1], candidate_a, loop_section)
            except StopIteration:
                continue
    raise StopIteration


def solve(inputs: str):
    registers_input, program_input = inputs.split("\n\n")
    program = list(map(int, program_input[8:].split(",")))
    register_a = int(registers_input.splitlines()[0][12:])
    print(f"Part 1: {','.join(map(str, run_program(program, register_a)))}")

    assert program[-2:] == [3, 0]
    loop_section = program[:-2]
    register_a = reverse_engineer(program, 0, loop_section)
    assert run_program(program, register_a) == program
    print(f"Part 2: {register_a}\n")


solve(example_input)
solve(actual_input)
