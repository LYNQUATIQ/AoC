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


def move_crates(arrangement: str, procedures: str, is_9001: bool = False) -> str:
    rows = arrangement.splitlines()
    columns = int((rows[-1][-2]))

    stacks: dict[int, deque[str]] = defaultdict(deque)
    for row in rows[:-1]:
        for column in range(columns):
            crate = row[column * 4 + 1]
            if crate != " ":
                stacks[column + 1].append(crate)

    for move in procedures.splitlines():
        n, column_1, column_2 = map(int, re.findall(r"\d+", move))
        moving = [stacks[column_1].popleft() for _ in range(n)]
        for crate in moving[::-1] if is_9001 else moving:
            stacks[column_2].appendleft(crate)

    return "".join([stacks[c + 1][0] for c in range(columns)])


def solve(inputs: str) -> None:
    arrangement, procedures = inputs.split("\n\n")

    print(f"\nPart 1: {move_crates(arrangement, procedures)}")
    print(f"Part 2: {move_crates(arrangement, procedures, is_9001=True)}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
