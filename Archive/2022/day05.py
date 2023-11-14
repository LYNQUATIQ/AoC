"""https://adventofcode.com/2022/day/5"""
import os
import re

from collections import defaultdict, deque
from itertools import product

with open(os.path.join(os.path.dirname(__file__), f"inputs/day05_input.txt")) as f:
    actual_input = f.read()


sample_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def move_crates(arrangement: str, procedures: str, is_9001: bool = False) -> str:

    stacks: dict[int, deque[str]] = defaultdict(deque)

    # Read arrangement into stacks data structure (dict of deques)
    rows = arrangement.splitlines()
    n_columns = int(rows.pop().split()[-1])
    for row, column in product(rows, range(n_columns)):
        crate = row[column * 4 + 1]
        if crate != " ":
            stacks[column + 1].append(crate)

    # Perform each move popping crates off one by one (re-reversing if crane is 9001)
    for move in procedures.splitlines():
        n, move_from, move_to = map(int, re.findall(r"\d+", move))
        moving = [stacks[move_from].popleft() for _ in range(n)]
        for crate in moving[::-1] if is_9001 else moving:
            stacks[move_to].appendleft(crate)

    # Return top (first) crate in each stack
    return "".join([stacks[c + 1][0] for c in range(n_columns)])


def solve(inputs: str) -> None:
    arrangement, procedures = inputs.split("\n\n")
    print(f"Part 1: {move_crates(arrangement, procedures)}")
    print(f"Part 2: {move_crates(arrangement, procedures, is_9001=True)}\n")


solve(sample_input)
solve(actual_input)
