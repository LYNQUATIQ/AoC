import logging
import os

from collections import defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

blacklists= []
for line in lines:
    a, b = (int(ip) for ip in line.split("-"))
    blacklists.append((a, b))
blacklists.sort()

MAXIMUM_IP = 4294967295
lowest_valid_ip = MAXIMUM_IP
valid_ips = 0

ip = 0
list_iter = iter((b for b in blacklists))
list_high = -1
while ip <= MAXIMUM_IP:
    while list_high < ip:
        list_low, list_high = next(list_iter)

    if ip < list_low:
        valid_ips += 1
        lowest_valid_ip = min(ip, lowest_valid_ip)
    else:
        ip = list_high

    ip += 1

print(f"Part 1: {lowest_valid_ip}")
print(f"Part 2: {valid_ips}")
