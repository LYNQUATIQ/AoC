import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

passwords = []
for line in lines:
    tokens = line.split(" ")
    a, b = tokens[0].split("-")
    a, b = int(a), int(b)
    character = tokens[1][0]
    password = tokens[2]
    passwords.append((a, b, character, password))

valid_passwords = 0
for min_count, max_count, character, password in passwords:
    letter_count = password.count(character)
    if letter_count >= min_count and letter_count <= max_count:
        valid_passwords += 1

print(f"Part 1: {valid_passwords}")

valid_passwords = 0
for pos1, pos2, character, password in passwords:
    if (password[pos1 - 1] == character) + (password[pos2 - 1] == character) == 1:
        valid_passwords += 1

print(f"Part 2: {valid_passwords}")
