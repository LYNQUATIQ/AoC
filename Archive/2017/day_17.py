import logging
import os
import time

from collections import deque

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_15.log")
logging.basicConfig(
    level=logging.WARNING, filename=log_file, filemode="w",
)

step_size = 328


def circular_buffer(length, step_size):
    buffer = deque([0])
    for value in range(length):
        buffer.rotate(-1 * step_size)
        buffer.append(value + 1)
    return buffer


t = time.time()
buffer = circular_buffer(2017, step_size)
print(f"Part 1: {buffer[0]}     ({time.time()-t}s)")

t = time.time()
buffer = circular_buffer(50000000, step_size)
print(f"Part 2: {buffer[buffer.index(0) + 1]}     ({time.time()-t}s)")
