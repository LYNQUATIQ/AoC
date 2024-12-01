import logging
import os

import datetime

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

answer = 0
for line in lines:
    inputs = list(map(int, line.split()))
    iterations = inputs[0]
    width = inputs[1]
    seeds = inputs[2:]

    adjacenies = defaultdict(set)
    for x in range(width):
        for y in range(width):
            xy = y * width + x
            if y > 0:
                adjacenies[xy].add((y - 1) * width + x)
            if y < width - 1:
                adjacenies[xy].add((y + 1) * width + x)
            if x > 0:
                adjacenies[xy].add(y * width + x - 1)
            if x < width - 1:
                adjacenies[xy].add(y * width + x + 1)

    board = set()
    for i in range(0, len(seeds) - 1, 2):
        xy = seeds[i + 1] * width + seeds[i]
        board.add(xy)

    def print_board(board, width):
        for x in range(width):
            for y in range(width):
                xy = y * width + x
                c = "#" if xy in board else "."
                print(c, end="")
            print("")
        print()

    states = {frozenset(board): 0}
    for iteration in range(iterations):
        newboard = set()
        for xy in range(width * width):
            if len(adjacenies[xy].intersection(board)) % 2:
                newboard.add(xy)
        try:
            key = frozenset(newboard)
            prior_state = states[key]
            board = states[(iterations - prior_state) % (iteration - prior_state)]
            break
        except KeyError:
            states[key] = iteration
            board = newboard

    answer += len(board)
    print(f"{line}\nANSWER:{len(board)}\n")

print(answer)
