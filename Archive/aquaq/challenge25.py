import logging
import os

import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

morse_dict = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
}

messages = []
timestamps = []
for line in lines:
    try:
        _, _, s = line.split(":")
        timestamps.append(float(s))
    except ValueError:
        messages.append(timestamps)
        timestamps = []
messages.append(timestamps)


def decode_timestamps(t1, t2):
    length = t2 - t1
    if length < 0:
        length += 60
    if length > 4:
        return " "
    if length > 2:
        return "-"
    return "."


for message in messages:
    plaintext = ""
    morse = ""
    for i in range(0, len(message), 2):
        morse += decode_timestamps(message[i], message[i + 1])
        try:
            space = decode_timestamps(message[i + 1], message[i + 2])
        except IndexError:
            space = "-"
        if space != ".":
            plaintext += morse_dict[morse]
            morse = ""
            if space == " ":
                plaintext += " "
            plaintext
    print(plaintext)
