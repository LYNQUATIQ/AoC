import logging
import os

from collections import defaultdict


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


class Bot:
    def __init__(self, number):
        self.number = number
        self.chips = []

    def is_running(self):
        return len(self.chips) == 2

    def receive_chip(self, value):
        assert len(self.chips) < 2
        self.chips.append(value)

    def give_chips(self):
        lower = min(self.chips)
        upper = max(self.chips)
        self.chips = []
        return lower, upper


rules = {}
bots = {}
outputs = {}


def get_bot(number):
    try:
        bot = bots[number]
    except KeyError:
        bot = Bot(number)
        bots[bot.number] = bot
    return bot


for line in lines:
    tokens = line.split(" ")
    if tokens[0] == "value":
        bot = get_bot(int(tokens[5]))
        bot.receive_chip(int(tokens[1]))
    else:
        rules[int(tokens[1])] = (
            (tokens[5], int(tokens[6])),
            (tokens[10], int(tokens[11])),
        )

while True:
    bot = None
    for b in bots.values():
        if b.is_running():
            bot = b
            break

    if bot is None:
        break

    if set(bot.chips) == set([17, 61]):
        part_1 = bot.number

    lower, upper = bot.give_chips()
    lower_destination, upper_destination = rules[bot.number]
    for value, destination in zip(
        [lower, upper], [lower_destination, upper_destination]
    ):
        dest, number = destination
        if dest == "output":
            outputs[number] = value
        else:
            bot = get_bot(number)
            bots[number].receive_chip(value)

print(f"Part 1: {part_1}")
print(f"Part 2: {outputs[0] * outputs[1] * outputs[2]}")
