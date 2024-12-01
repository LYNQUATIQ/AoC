import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
input_signal = [line.rstrip("\n") for line in open(input_file)][0]

PHASES = 100

current_list = [int(d) for d in input_signal]
digit_count = len(current_list) + 1
for _ in range(PHASES):
    new_list = []
    for row in range(1, digit_count):
        total = 0
        for column, d in enumerate(current_list, 1):
            p = (column // row) % 4
            p = (p % 2) * (2 - p)
            total += p * d
        new_list.append(abs(total) % 10)
    current_list = new_list

print(f"Part 1: {''.join(str(d) for d in current_list[0:8])}")


message_offset = int(input_signal[0:7])
current_list = [int(d) for d in input_signal * 10000]
tail_list = current_list[message_offset:]
tail_length = len(tail_list) - 1
for _ in range(PHASES):
    for i in range(tail_length - 1, 0, -1):
        tail_list[i - 1] = (tail_list[i - 1] + tail_list[i]) % 10

print(f"Part 2: {''.join(str(d) for d in tail_list[0:8])}")
