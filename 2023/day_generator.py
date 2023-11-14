""" Generates daily py files for AOC"""
import os

YYYY = 2023


for i in range(1, 26):
    with open(
        os.path.join(os.path.dirname(__file__), f"inputs/day{i:02d}_input.txt"), "w"
    ):
        pass

    with open(os.path.join(os.path.dirname(__file__), f"day{i:02d}.py"), "w") as f:
        f.write(f'"""https://adventofcode.com/{YYYY}/day/{i}"""\n')
        f.write("import os\n\n")
        f.write(
            f'with open(os.path.join(os.path.dirname(__file__), f"inputs/day{i:02d}_input.txt")) as f:\n'
        )
        f.write("    actual_input = f.read()\n\n\n")
        f.write('sample_input = """xxx"""\n\n\n')
        f.write("def solve(inputs):\n")
        f.write("    values = tuple(map(int, inputs.splitlines()))\n\n")
        f.write('    print(f"Part 1: {False}")\n')
        f.write('    print(f"Part 2: {False}")\n\n\n')
        f.write("solve(sample_input)\n")
        f.write("# solve(actual_input)\n")
