import logging
import os
import re

from collections import defaultdict

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_8.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, "inputs/2017_day_8_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


registers = defaultdict(int)
max_register_value = 0
pattern = re.compile(
    r"^(?P<register>[a-z]+) (?P<inc_dec>[a-z]{3}) (?P<delta>-?\d+) if (?P<cond_register>[a-z]+) (?P<condition>[<>=!]+) (?P<cond_value>-?\d+)$"
)
for line in lines:
    params = pattern.match(line).groupdict()
    register = params["register"]
    delta = int(params["delta"])
    if params["inc_dec"] == "dec":
        delta *= -1
    r = params["cond_register"]
    v = int(params["cond_value"])
    condition = params["condition"]
    if condition == "!=":
        do_it = registers[r] != v
    elif condition == "==":
        do_it = registers[r] == v
    elif condition == ">=":
        do_it = registers[r] >= v
    elif condition == "<=":
        do_it = registers[r] <= v
    elif condition == ">":
        do_it = registers[r] > v
    elif condition == "<":
        do_it = registers[r] < v
    if do_it:
        registers[register] += delta
    max_register_value = max(max_register_value, max(registers.values()))


print(f"Part 1: {max(registers.values())}")
print(f"Part 2: {max_register_value}")
