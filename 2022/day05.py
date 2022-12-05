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

    columns = int((rows[-1][-2]))

    stacks_9000: dict[int, deque[str]] = defaultdict(deque)
    stacks_9001: dict[int, deque[str]] = defaultdict(deque)

    for row in rows[:-1]:
        for column in range(1, columns + 1):
            crate = row[column * 4 - 3]
            if crate != " ":
                stacks_9000[column].append(crate)
                stacks_9001[column].append(crate)

    for move in moves:
        n, column_1, column_2 = map(int, re.findall(r"\d+", move))

        for _ in range(n):
            stacks_9000[column_2].appendleft(stacks_9000[column_1].popleft())

        moving = [stacks_9001[column_1].popleft() for _ in range(n)]
        for crate in moving[::-1]:
            stacks_9001[column_2].appendleft(crate)

    print(f"\nPart 1: {''.join([stacks_9000[c][0] for c in range(1, columns + 1)])}")
    print(f"Part 2: {''.join([stacks_9001[c][0] for c in range(1, columns + 1)])}\n")


solve(SAMPLE_INPUT)
solve(actual_input)
