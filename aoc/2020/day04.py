import os
import re

with open(os.path.join(os.path.dirname(__file__), "inputs/day04_input.txt")) as f:
    actual_input = f.read()

sample_input = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
sample_input = sample_input


class Passport:
    @staticmethod
    def _valid_number(x, min_value, max_value):
        return x.isdigit() and min_value <= int(x) <= max_value

    @staticmethod
    def _valid_height(x, valid_heights):
        try:
            height, units = re.match(rf"^(\d+)({'|'.join(valid_heights)})$", x).groups()
        except AttributeError:
            return False
        return Passport._valid_number(height, *valid_heights[units])

    DETAIL_CHECKS = {
        "byr": lambda x: Passport._valid_number(x, 1920, 2002),
        "iyr": lambda x: Passport._valid_number(x, 2010, 2020),
        "eyr": lambda x: Passport._valid_number(x, 2020, 2030),
        "hgt": lambda x: Passport._valid_height(x, {"cm": (150, 193), "in": (59, 76)}),
        "hcl": lambda x: re.match(r"^#[0-9a-f]{6}$", x),
        "ecl": lambda x: re.match(r"^amb|blu|brn|gry|grn|hzl|oth$", x),
        "pid": lambda x: re.match(r"^\d{9}$", x),
        "cid": lambda x: True,
    }

    def __init__(self, raw_input):
        self.details = dict(token.split(":") for token in raw_input.split())

    def has_required_fields(self):
        required_details = set(self.DETAIL_CHECKS.keys())
        required_details.discard("cid")
        return required_details.issubset(self.details)

    def fields_valid(self):
        return all(self.DETAIL_CHECKS[k](v) for k, v in self.details.items())


def solve(inputs):
    passports = [Passport(tokens) for tokens in inputs.split("\n\n")]

    part1, part2 = 0, 0
    for passport in passports:
        if passport.has_required_fields():
            part1 += 1
            part2 += passport.fields_valid()

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(sample_input)
solve(actual_input)
