import logging
import os

import hashlib

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

door_id = "ojvtpuvg"

integer = 0
door_code = ""
while True:
    input_str = f"{door_id}{integer}"
    result = hashlib.md5(input_str.encode())
    hex_output = result.hexdigest()
    if hex_output[0:5] == "00000":
        door_code += hex_output[5]
        print(f"{integer:>10} - door code: [{door_code + '-' * (8 - len(door_code))}]")
        if len(door_code) == 8:
            break
    integer += 1

print(f"Part 1: {door_code}")


integer = 0
door_code = "--------"
while True:
    input_str = f"{door_id}{integer}"
    result = hashlib.md5(input_str.encode())
    hex_output = result.hexdigest()
    if hex_output[0:5] == "00000" and hex_output[5] in "01234567":
        position = int(hex_output[5])
        if door_code[position] == "-":
            door_code = door_code[:position] + hex_output[6] + door_code[position + 1 :]
            print(f"{integer:>10} - door code: [{door_code}]")
            if not "-" in door_code:
                break
    integer += 1

print(f"Part 2: {door_code}")
