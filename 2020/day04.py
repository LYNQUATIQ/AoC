import logging
import os
import re

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

passports = defaultdict(dict)
passport = None
for i, line in enumerate(lines):
    if line == "":
        passport = None
        continue
    passport = passport or passports[i]
    passport.update([token.split(":") for token in line.split()])


def is_valid_number(x, min_value, max_value):
    return re.match(r"^\d+$", x) and min_value <= int(x) <= max_value


def is_valid_height(x, valid_heights):
    try:
        height, measure = re.search(rf"^(\d+)({'|'.join(valid_heights)})$", x).groups()
    except AttributeError:
        return False
    return is_valid_number(height, *valid_heights[measure])


detail_checks = {
    "byr": lambda x: is_valid_number(x, 1920, 2002),
    "iyr": lambda x: is_valid_number(x, 2010, 2020),
    "eyr": lambda x: is_valid_number(x, 2020, 2030),
    "hgt": lambda x: is_valid_height(x, {"cm": (150, 193), "in": (59, 76)}),
    "hcl": lambda x: re.match(r"^#[0-9a-f]{6}$", x),
    "ecl": lambda x: re.match(r"^amb|blu|brn|gry|grn|hzl|oth$", x),
    "pid": lambda x: re.match(r"^\d{9}$", x),
    "cid": lambda x: True,
}

required_details = set(detail_checks.keys())
required_details.discard("cid")

part1, part2 = 0, 0
for passport_details in passports.values():
    if required_details.issubset(passport_details):
        part1 += 1
        part2 += all(detail_checks[k](v) for k, v in passport_details.items())

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
