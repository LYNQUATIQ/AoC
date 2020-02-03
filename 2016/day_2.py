import logging
import os


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/day_2.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/day_2_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

directions = {
    "1" : {"U": "1", "L": "1", "R": "2", "D": "4"},
    "2" : {"U": "2", "L": "1", "R": "3", "D": "5"},
    "3" : {"U": "3", "L": "2", "R": "3", "D": "6"},
    "4" : {"U": "1", "L": "4", "R": "5", "D": "7"},
    "5" : {"U": "2", "L": "4", "R": "6", "D": "8"},
    "6" : {"U": "3", "L": "5", "R": "6", "D": "9"},
    "7" : {"U": "4", "L": "7", "R": "8", "D": "7"},
    "8" : {"U": "5", "L": "7", "R": "9", "D": "8"},
    "9" : {"U": "6", "L": "8", "R": "9", "D": "9"},
}

code = ""
digit = "5"
for line in lines:
    for d in line:
        digit = directions[digit][d]
    code += digit

print(f"Part 1: {code}")


directions = {
    "1" : {"U": "1", "L": "1", "R": "1", "D": "3"},
    "2" : {"U": "2", "L": "2", "R": "3", "D": "6"},
    "3" : {"U": "1", "L": "2", "R": "4", "D": "7"},
    "4" : {"U": "4", "L": "3", "R": "4", "D": "8"},
    "5" : {"U": "5", "L": "5", "R": "6", "D": "5"},
    "6" : {"U": "2", "L": "5", "R": "7", "D": "A"},
    "7" : {"U": "3", "L": "6", "R": "8", "D": "B"},
    "8" : {"U": "4", "L": "7", "R": "9", "D": "C"},
    "9" : {"U": "9", "L": "8", "R": "9", "D": "9"},
    "A" : {"U": "6", "L": "A", "R": "B", "D": "A"},
    "B" : {"U": "7", "L": "A", "R": "C", "D": "D"},
    "C" : {"U": "8", "L": "B", "R": "C", "D": "C"},
    "D" : {"U": "B", "L": "D", "R": "D", "D": "D"},
}

code = ""
digit = "5"
for line in lines:
    for d in line:
        digit = directions[digit][d]
    code += digit

print(f"Part 2: {code}")