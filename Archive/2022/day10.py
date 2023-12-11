"""https://adventofcode.com/2022/day/10"""
import os

with open(os.path.join(os.path.dirname(__file__), "inputs/day10_input.txt")) as f:
    actual_input = f.read()


sample_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


LIT, DARK = "\u2588", " "


def solve(inputs: str) -> None:
    x_register, cycle, signal_strength = 1, 0, 0
    raster = ""

    def next_cycle():
        nonlocal cycle, raster, signal_strength
        raster += LIT if abs(x_register - cycle % 40) <= 1 else DARK
        cycle += 1
        if (cycle + 20) % 40 == 0:
            signal_strength += cycle * x_register

    for instruction, *values in tuple(map(str.split, inputs.splitlines())):
        next_cycle()
        if instruction == "addx":
            next_cycle()
            x_register += int(values[0])

    print(f"\nPart 1: {signal_strength}")
    print("Part 2:")
    for i in range(0, len(raster), 40):
        print(raster[i : i + 40])


solve(sample_input)
solve(actual_input)
