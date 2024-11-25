import logging
import os
import re


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_22.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=file_path,
    filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_22_input.txt")
lines = [line.rstrip("\n") for line in open(file_path)]

pattern = re.compile(
    "^(?P<shuffle>deal with increment|cut|deal into new stack)\s?(?P<amount>-?\d*)$"
)

shuffles = []
for line in lines:
    regex_groups = pattern.match(line).groupdict()
    try:
        amount = int(regex_groups["amount"])
    except ValueError:
        amount = None
    shuffles.append((regex_groups["shuffle"], amount))

NUMBER_OF_CARDS = 10007
NUMBER_OF_CARDS = 119315717514047

NUMBER_OF_SHUFFLES = 1
NUMBER_OF_SHUFFLES = 101741582076661


def adjust_offset_increment(offset, increment, shuffle, amount):
    if shuffle == "cut":
        offset += increment * amount
    elif shuffle == "deal into new stack":
        increment *= -1
        offset += increment
    elif shuffle == "deal with increment":
        increment *= pow(amount, NUMBER_OF_CARDS - 2, NUMBER_OF_CARDS)
    return offset, increment


# Single pass
offset, increment = 0, 1
for shuffle, amount in shuffles:
    offset, increment = adjust_offset_increment(offset, increment, shuffle, amount)


# Multiple passes
offset *= pow(1 - increment, NUMBER_OF_CARDS - 2, NUMBER_OF_CARDS)
increment = pow(increment, NUMBER_OF_SHUFFLES, NUMBER_OF_CARDS)


print((2020 * increment + (1 - increment) * offset) % NUMBER_OF_CARDS)
