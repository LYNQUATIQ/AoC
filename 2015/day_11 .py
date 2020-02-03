import logging
import os

import re

from itertools import groupby

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)


def increment_password(password):
    def increment_character(c):
        if c == "z":
            return "a"        
        c = chr(ord(c) + 1)
        if c in "ilo":
            c = increment_character(c)
        return c
    
    i = len(password) - 1
    while True:
        next_character = increment_character(password[i])
        password = password[:i] + next_character + password[i+1:]
        if next_character != "a":
            break
        i = i - 1
    
    return password

two_pairs = re.compile(r"^\w*(\w)(\1)\w*(\w)(\3)\w*$")

password = "cqjxjnds"

def next_valid_password(password):
    while True:
        password = increment_password(password)
        found_seq = False
        for i in range(len(password) - 3):
            if ord(password[i + 1]) - ord(password[i]) == 1 and ord(password[i + 2]) - ord(password[i + 1]) == 1:
                found_seq = True
                break
        found_pairs = two_pairs.match(password) is not None
        if found_seq and found_pairs:
            break
    return password

password = next_valid_password(password)
print(f"Part 1: {password}")


password = next_valid_password(password)
print(f"Part 2: {password}")
