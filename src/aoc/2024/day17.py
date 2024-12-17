"""https://adventofcode.com/2024/day/17"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 17)


example_input = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

example_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

REGISTER_A, REGISTER_B, REGISTER_C = "A", "B", "C"


def combo(operand, registers):
    if operand <= 3:
        return operand
    if operand == 4:
        return registers[REGISTER_A]
    if operand == 5:
        return registers[REGISTER_B]
    if operand == 6:
        return registers[REGISTER_C]
    raise ValueError(f"Invalid combo operand {operand}")


def run_program(
    program: list[int], register_a: int, check_for_match: bool = False
) -> list[int]:
    registers = {REGISTER_A: register_a, REGISTER_B: 0, REGISTER_C: 0}
    pointer, output = 0, []
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]
        if opcode == 0:  # adv
            registers[REGISTER_A] //= 2 ** combo(operand, registers)
        elif opcode == 1:  # bxl
            registers[REGISTER_B] ^= operand
        elif opcode == 2:  # bst
            registers[REGISTER_B] = combo(operand, registers) % 8
        elif opcode == 3:  # jnz
            if registers[REGISTER_A] != 0:
                pointer = operand
                continue
        elif opcode == 4:  # bxl
            registers[REGISTER_B] ^= registers[REGISTER_C]
        elif opcode == 5:  # out
            output.append(combo(operand, registers) % 8)
            if check_for_match and output != program[: len(output)]:
                return []
        elif opcode == 6:  # bdv
            registers[REGISTER_B] = registers[REGISTER_A] // (
                2 ** combo(operand, registers)
            )
        elif opcode == 7:  # cdv
            registers[REGISTER_C] = registers["A"] // (2 ** combo(operand, registers))
        pointer += 2
    return output


def solve(inputs: str):
    registers_input, program_input = inputs.split("\n\n")
    program = list(map(int, program_input[8:].split(",")))
    register_a = int(registers_input.splitlines()[0][12:])
    output = run_program(program, register_a)
    print(f"Part 1: {','.join(map(str, output))}")

    register_a = 0
    while run_program(program, register_a, check_for_match=True) != program:
        register_a += 1
    print(f"Part 2: {register_a}\n")


solve(example_input)
solve(actual_input)
