import logging
import os


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_13.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/2017_day_13_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

scanners = []
for line in lines:
    layer, depth = (int(d) for d in line.split(": "))
    scanners.append((layer, depth))


def severity(delay=0):
    severity = 0
    for layer, depth in scanners:
        if (delay + layer) % (2 * (depth -1)) == 0:
            severity += layer * depth
    return severity

print(f"Part 1: {severity()}")


def got_caught(delay):
    for layer, depth in scanners:
        if (delay + layer) % (2 * (depth -1)) == 0:
            return True
    return False

delay = 1
while got_caught(delay):
    delay += 1

print(f"Part 2: {delay}")

