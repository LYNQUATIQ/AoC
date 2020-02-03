import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w")

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


literal_characters = 0
encoded_characters = 0
for line in lines:
    literal_characters += len(line)
    encoded_string = line[1:-1]
    i = 0
    while True:
        try:
            this_char = encoded_string[i]
        except IndexError:
            break
        if this_char == "\\":
            try:
                next_char = encoded_string[i + 1]
            except IndexError:
                break
            if next_char == "\\" or next_char == '"':
                i += 1
                this_char = next_char
            elif next_char == "x":
                try:
                    _ = int(encoded_string[i + 2 : i + 4], 16)
                except (IndexError, ValueError):
                    pass
                i += 3
        encoded_characters += 1
        i += 1

print(f"Part 1: {literal_characters - encoded_characters}")

encoded_characters = 0
literal_characters = 0
for line in lines:
    encoded_characters += len(line)
    literal_characters += 2
    i = 0
    while True:
        try:
            if line[i] in ["\\", '"']:
                literal_characters += 1
            literal_characters += 1
        except IndexError:
            break
        i += 1

print(f"Part 2: {literal_characters - encoded_characters}")

