import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

initial_state = "10010000000110000"

def fill_disk(state, length):
    while len(state) < length:
        a = state
        b = a[::-1]
        b = "".join([{"1":"0", "0":"1"}[d] for d in b])
        state = a + "0" + b
    return state


def checksum(data):
    if len(data) % 2 == 1:
        return data
    output = ""
    for i in range(0, len(data), 2):
        if data[i] == data[i+1]:
            output += "1"
        else:
            output += "0"
    return checksum(output)

length = 272
data = fill_disk(initial_state, length)
print(f"Part 1: {checksum(data[:length])}")

length = 35651584
data = fill_disk(initial_state, length)
print(f"Part 2: {checksum(data[:length])}")
