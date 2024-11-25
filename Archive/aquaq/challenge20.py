import logging
import os

import datetime

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]


input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

cards = lines[0].split()
wins = 0
running_total = 0
ace_count = 0
for card in cards:

    print(f"Draw a {card}: current total of ", end="")
    if card in "JQK":
        running_total += 10
    elif card == "A":
        running_total += 1
        ace_count += 1
    else:
        running_total += int(card)
    totals = [running_total] + list(
        (running_total + (x + 1) * 10 for x in range(ace_count))
    )
    print(" or ".join([str(x) for x in totals]))
    if any(x == 21 for x in totals):
        wins += 1
        running_total = 0
        ace_count = 0
        print("This is a win!")
        continue

    if running_total > 21:
        running_total = 0
        ace_count = 0
        print("This is a loss. Start again with the next card:")

print(wins)
