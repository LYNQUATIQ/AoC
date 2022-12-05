"""https://adventofcode.com/2022/day/5"""
import os
import re

from collections import defaultdict, deque

with open(os.path.join(os.path.dirname(__file__), f"inputs/day05_input.txt")) as f:
    actual_input = f.read()


SAMPLE_INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def solve(inputs: str) -> None:
    arrangement, procedures = inputs.split("\n\n")
    rows = arrangement.splitlines()
    moves = procedures.splitlines()

    stacks = defaultdict(deque)
    columns = int((rows[-1][-2]))
    for row in rows[:-1]:
        for column in range(1, columns + 1):
            crate = row[column * 4 - 3]
            if crate != " ":
                stacks[column].append(crate)

    for move in moves:
        n, column_1, column_2 = map(int, re.findall(r"\d+", move))
        for _ in range(n):
            stacks[column_2].appendleft(stacks[column_1].popleft())

    top_row = ""
    for column in range(1, columns + 1):
        top_row += stacks[column][0]

    print(f"\nPart 1: {top_row}")

    stacks = defaultdict(deque)
    columns = int((rows[-1][-2]))
    for row in rows[:-1]:
        for column in range(1, columns + 1):
            crate = row[column * 4 - 3]
            if crate != " ":
                stacks[column].append(crate)

    for move in moves:
        n, column_1, column_2 = map(int, re.findall(r"\d+", move))
        moving = [stacks[column_1].popleft() for _ in range(n)]
        for crate in moving[::-1]:
            stacks[column_2].appendleft(crate)

    top_row = ""
    for column in range(1, columns + 1):
        top_row += stacks[column][0]

    print(f"Part 2: {top_row}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
