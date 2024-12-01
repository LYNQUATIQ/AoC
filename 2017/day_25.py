import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2018_day_25.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

actions = {
    "A": {0: (1, +1, "B"), 1: (0, -1, "C")},
    "B": {0: (1, -1, "A"), 1: (1, -1, "D")},
    "C": {0: (1, +1, "D"), 1: (0, +1, "C")},
    "D": {0: (0, -1, "B"), 1: (0, +1, "E")},
    "E": {0: (1, +1, "C"), 1: (1, -1, "F")},
    "F": {0: (1, -1, "E"), 1: (1, +1, "A")},
}

state = "A"
steps = 12172063

tape = defaultdict(int)
cursor = 0
for _ in range(steps):
    write_value, move, state = actions[state][tape[cursor]]
    tape[cursor] = write_value
    cursor += move

print(f"Part 1: {sum(tape.values())}")
