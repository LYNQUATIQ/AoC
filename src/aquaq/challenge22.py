import logging
import os

import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
inputs = [int(v) for v in lines[0].split()]

roman_dict = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    90: "XC",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I",
}
values = sorted(roman_dict.keys(), reverse=True)

cypher = {k: v for v, k in enumerate(string.ascii_uppercase, 1)}


def int_to_roman(number):
    roman = ""
    i = 0
    while number > 0:
        value = values[i]
        for _ in range(number // value):
            roman += roman_dict[value]
            number -= value
        i += 1
    return roman


answer = 0
for number in inputs:
    answer += sum([cypher[c] for c in int_to_roman(number)])

print(answer)
