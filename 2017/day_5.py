import logging
import os


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_5.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/2017_day_5_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

program = [int(line) for line in lines]

i = 0
steps = 0
while True:
    try:
        jump = program[i]
    except IndexError:
        break
    program[i] += 1
    i += jump
    steps += 1

print(f"Part 1: {steps}")

program = [int(line) for line in lines]

i = 0
steps = 0
while True:
    try:
        jump = program[i]
    except IndexError:
        break
    if jump >= 3:
        program[i] -= 1
    else:
        program[i] += 1
    i += jump
    steps += 1

print(f"Part 2: {steps}")