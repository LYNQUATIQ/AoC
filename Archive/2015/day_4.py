import logging
import os

import hashlib

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

input_txt = "ckczppom"
# input_txt = "abcdef"


def get_answer(num_zeroes):
    integer = 0
    while True:
        input_str = f"{input_txt}{integer}"
        result = hashlib.md5(input_str.encode())
        hex_output = result.hexdigest()
        if hex_output[0:num_zeroes] == "0" * num_zeroes:
            break
        integer += 1
    return integer


print(f"Part 1: {get_answer(5)}")
print(f"Part 2: {get_answer(6)}")
