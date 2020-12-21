import json
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day12_input.txt")) as f:
    actual_input = f.read()


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


def solve(inputs):
    data = json.loads(inputs)
    print(f"Part 1: {get_item_total(data)}")
    print(f"Part 2: {get_item_total(data, ignore_reds=True)}")


solve(actual_input)