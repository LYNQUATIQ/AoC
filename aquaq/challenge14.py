import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

bingo_card = [
    [6, 17, 34, 50, 68],
    [10, 21, 45, 53, 66],
    [5, 25, 36, 52, 69],
    [14, 30, 33, 54, 63],
    [15, 23, 41, 51, 62],
]
winning_lines = []
diagonal1 = set()
diagonal2 = set()
for i in range(5):
    row = set()
    column = set()
    diagonal1.add(bingo_card[i][i])
    diagonal2.add(bingo_card[i][4 - i])
    for j in range(5):
        row.add(bingo_card[i][j])
        column.add(bingo_card[j][i])
    winning_lines.append(row)
    winning_lines.append(column)
winning_lines.append(diagonal1)
winning_lines.append(diagonal2)

answer = 0
for input_line in lines:
    calls = list(map(int, input_line.split()))
    for i in range(5, len(calls)):
        call_set = set(calls[:i])
        if any([line.issubset(call_set) for line in winning_lines]):
            answer += i
            break

print(answer)
