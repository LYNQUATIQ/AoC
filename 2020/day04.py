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
    if passport is None:
        passport = passports[i]
    tokens = line.split(" ")
    for token in tokens:
        k, v = token.split(":")
        passport[k] = v

required = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

part1 = 0
for passport in passports.values():
    if required.issubset(passport.keys()):
        part1 += 1
print(f"Part 1: {part1}")


def match_value(value, min_value, max_value):
    if not re.match(r"^\d+$", value):
        return False
    value = int(value)
    return value >= min_value and value <= max_value


part2 = 0
for line, passport in passports.items():
    if not required.issubset(passport.keys()):
        continue

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if not match_value(passport["byr"], 1920, 2002):
        continue

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if not match_value(passport["iyr"], 2010, 2020):
        continue

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not match_value(passport["eyr"], 2020, 2030):
        continue

    # hgt (Height) - a number followed by either cm or in:
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    hgt = re.search(r"^(\d+)(\w{2})$", passport["hgt"])
    if hgt is None:
        continue
    hgt, measure = hgt.groups()
    valid_hgt = False
    if measure == "cm":
        valid_hgt = match_value(hgt, 150, 193)
    elif measure == "in":
        valid_hgt = match_value(hgt, 59, 76)
    if not valid_hgt:
        continue

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not re.match(r"^#[0-9a-f]{6}$", passport["hcl"]):
        continue

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        continue

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.match(r"^\d{9}$", passport["pid"]):
        continue

    part2 += 1

print(f"Part 2: {part2}")
