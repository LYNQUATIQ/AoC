import logging
import os

from collections import defaultdict, deque
from itertools import cycle

from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_23.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)

file_path = os.path.join(script_dir, "inputs/day_23_input.txt")
with open(file_path) as f:
    program_str = f.read()
program = [int(x) for x in program_str.split(",")]


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


class Address255(Exception):
    pass


NUMBER_OF_NIC_COMPUTERS = 50
NAT_ADDRESS = 255

nic_computers = {}
nic_queues = defaultdict(deque)

for addr in range(NUMBER_OF_NIC_COMPUTERS):
    computer = IntCodeComputer(program)
    nic_computers[addr] = computer
    computer.run_program([addr])

addr_looper = cycle(range(NUMBER_OF_NIC_COMPUTERS))
number_in_queue = 0
last_nat_xy = None
last_nat_delivered_y = None
idle_counter = 0
while True:
    addr = next(addr_looper)
    computer = nic_computers[addr]
    queue = nic_queues[addr]
    while True:
        # print(f"Checking queue for #{addr} - {queue}")
        try:
            (x, y) = queue.popleft()
            computer.run_program([x, y])
            # print(f"Sending ({x}, {y}) to #{addr}... output: {computer.output()}")
        except IndexError:
            break
    computer.run_program([-1])

    idle_counter += 1
    for a, x, y in chunker(computer.output(clear_output=True), 3):
        # print(f"Processing ({a}, {x}, {y})")
        idle_counter = 0
        if a == 255:
            last_nat_xy = (x, y)
            # print(f"Storing {last_nat_xy} in NAT... queue = {number_in_queue}")
        else:
            nic_queues[a].append((x, y))

    if idle_counter > 50:
        idle_counter = 0
        print(f"Network idle... sending {last_nat_xy} to #0")
        x, y = last_nat_xy
        nic_queues[0].append([x, y])
        if y == last_nat_delivered_y:
            print(f"Last y delivered twice in row to #0... {y}")
            raise Address255
        last_nat_delivered_y = y
