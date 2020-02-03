import logging
import os
import re

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_9.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/2017_day_9_input.txt")

stream = []
with open(input_file) as f:
    while True:
        c = f.read(1)
        if not c:
            break
        stream.append(c)

# stream = [c for c in "{{},{}}"]
# stream = [c for c in "{{<!!>},{<!!>},{<!!>},{<!!>}}"]

class Group:
    def __init__(self, parent):
        self.parent = parent

current_depth = 0
groups = {}
group_counter = 0
pointer = 0
garbage = False
total_score = 0
garbage_count = 0
current_group = None
while True:
    try:
        c = stream[pointer]
        pointer += 1
    except IndexError:
        break

    if garbage and c == "!":
        pointer += 1
        continue

    if garbage:
        if c == ">":
            garbage = False
        else:
            garbage_count += 1
        continue

    if c == "{":
        current_group = Group(current_group)
        group_counter += 1
        current_depth += 1
        groups["Group " + str(group_counter)] = current_group
    elif c == "}":
        total_score += current_depth
        current_depth -= 1
        if current_depth > 0:
            current_group = current_group.parent
        else:
            current_group = None
    elif c == "<":
        garbage = True


print(f"Part 1: {total_score}")
print(f"Part 1: {garbage_count}")
