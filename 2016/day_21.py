import logging
import os

from collections import deque


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


def password_dict(password):
    return {i: c for i, c in enumerate(password)}


def password_string(password_dict):
    return "".join([password_dict[i] for i in range(len(password_dict))])


def swap_position(password, x, y):
    d = password_dict(password)
    d[x], d[y] = d[y], d[x]
    return password_string(d)


def swap_letter(password, x, y):
    return swap_position(password, password.find(x), password.find(y))


def rotate(password, x):
    d = deque(password)
    d.rotate(x)
    return "".join([c for c in d])


def reverse(password, x, y):
    return password[:x] + password[x : y + 1][::-1] + password[y + 1 :]


def move_position(password, x, y):
    c = password[x]
    p = password[:x] + password[x + 1 :]
    return p[:y] + c + p[y:]


def hash_password(password, lines, do_reverse=False):
    rotate_based_dict = {i: 1 + (i >= 4) + i for i in range(len(password))}
    if do_reverse:
        rotate_based_dict = {
            (v + k) % len(password): -v for k, v in rotate_based_dict.items()
        }

    for line in lines:
        tokens = line.split(" ")
        instruction = tokens[0] + " " + tokens[1]
        prior_password = password
        if instruction == "swap position":
            password = swap_position(password, int(tokens[2]), int(tokens[5]))
        elif instruction == "swap letter":
            password = swap_letter(password, tokens[2], tokens[5])
        elif instruction == "rotate left":
            r = int(tokens[2]) * -1
            if do_reverse:
                r = r * -1
            password = rotate(password, r)
        elif instruction == "rotate right":
            r = int(tokens[2])
            if do_reverse:
                r = r * -1
            password = rotate(password, r)
        elif instruction == "rotate based":
            i = password.find(tokens[6])
            r = rotate_based_dict[i]
            password = rotate(password, r)
        elif instruction == "reverse positions":
            password = reverse(password, int(tokens[2]), int(tokens[4]))
        elif instruction == "move position":
            x, y = int(tokens[2]), int(tokens[5])
            if do_reverse:
                x, y = y, x
            password = move_position(password, x, y)
        else:
            print(f"Can't read line: {line}")
            raise NotImplementedError
        logging.debug(f"{prior_password} - {line:38} >>> {password}")
    return password


print(f"Part 1: {hash_password('abcdefgh', lines)}")
print(f"Part 2: {hash_password('fbgdceah', lines[::-1], True)}")
