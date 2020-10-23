import logging
import os

import json

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]


def get_item_total(item, ignore_reds=False):
    if type(item) is int:
        return item
    elif type(item) is list:
        return sum(get_item_total(i, ignore_reds) for i in item)
    elif type(item) is dict:
        if ignore_reds and "red" in item.values():
            return 0
        return sum(get_item_total(i, ignore_reds) for i in item.values())
    return 0


data = json.loads(lines[0])

print(f"Part 1: {get_item_total(data)}")
print(f"Part 2: {get_item_total(data, ignore_reds=True)}")

