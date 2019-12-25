import logging
import math
import os
import time

from itertools import cycle

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "logs/day_16.log")
logging.basicConfig(
    level=logging.DEBUG, filename=file_path, filemode="w",
)


file_path = os.path.join(script_dir, "inputs/day_16_input.txt")
with open(file_path) as f:
    input_signal = f.read()

# input_signal = "03036732577212944063491565474664"
# input_signal = "12345678"

current_list = [int(d) for d in input_signal]
digit_count = len(current_list) + 1
phases = 100


start_time = time.time()
for _ in range(phases):
    new_list = []
    for row in range(1, digit_count):
        total = 0
        for column, d in enumerate(current_list, 1):
            p = (column // row) % 4
            p = (p % 2) * (2 - p)
            total += p * d
        total = abs(total) % 10
        new_list.append(total)
    current_list = new_list

print(
    f"After phase: {phases}: {''.join(str(d) for d in current_list[0:8])} - elapsed time: {time.time()-start_time}"
)

start_time = time.time()

message_offset = int(input_signal[0:7])
current_list = [int(d) for d in input_signal * 10000]
tail_list = current_list[message_offset:]
tail_length = len(tail_list) - 1
for _ in range(100):
    for i in range(tail_length - 1, 0, -1):
        tail_list[i - 1] = (tail_list[i - 1] + tail_list[i]) % 10

print(
    f"After phase: {phases}: {''.join(str(d) for d in tail_list[0:8])} - elapsed time: {time.time()-start_time}"
)

