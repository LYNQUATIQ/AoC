import logging
import os

from collections import Counter

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

TRAP = "^"
SAFE = "."

def find_traps(n_rows, first_row):
    rows = { 0: first_row }
    row_indices = { first_row: 0 }
    for i in range(n_rows):
        try:
            row = rows[i]
        except KeyError:
            prior_row = rows[i-1]
            try:
                row = rows[row_indices[prior_row] + 1]
            except KeyError:
                row = ""
                for x in range(len(prior_row)):
                    if x == 0:
                        left = SAFE
                    else: 
                        left = prior_row[x - 1]
                    if x == len(prior_row) - 1:
                        right = SAFE
                    else: 
                        right = prior_row[x + 1]
                    centre = prior_row[x]
                    if left == TRAP and centre == TRAP and right == SAFE:
                        row += TRAP
                        continue
                    if right == TRAP and centre == TRAP and left == SAFE:
                        row += TRAP
                        continue
                    if right == TRAP and centre == SAFE and left == SAFE:
                        row += TRAP
                        continue
                    if left == TRAP and centre == SAFE and right == SAFE:
                        row += TRAP
                        continue
                    row += SAFE
                rows[i] = row
                row_indices[row] = i
    return rows

first_row = "^^^^......^...^..^....^^^.^^^.^.^^^^^^..^...^^...^^^.^^....^..^^^.^.^^...^.^...^^.^^^.^^^^.^^.^..^.^"

traps = find_traps(40, first_row)
print(f"Part 1: {sum(Counter(row).get(SAFE, 0) for row in traps.values())}")

traps = find_traps(400000, first_row)
print(f"Part 2: {sum(Counter(row).get(SAFE, 0) for row in traps.values())}")

