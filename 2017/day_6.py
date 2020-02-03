import logging
import os


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_6.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

puzzle_input = "0	5	10	0	11	14	13	4	11	8	8	7	1	4	12	11"
# puzzle_input = "0	2	7	0"

memory_banks = [int(d) for d in puzzle_input.split("\t")]
print(memory_banks)

num_banks = len(memory_banks)
prior_states = set([tuple(memory_banks)])
redistribution_cycles = 0
while True:
    redistribution_cycles += 1
    to_redistribute = max(memory_banks)
    i = memory_banks.index(to_redistribute)
    memory_banks[i] = 0
    delta = max(to_redistribute // (num_banks - 1), 1)
    while to_redistribute:
        i = (i + 1) % num_banks
        amount_added = min(to_redistribute, delta)
        memory_banks[i] += amount_added
        to_redistribute -= amount_added

    if tuple(memory_banks) in prior_states:
        break
    prior_states.add(tuple(memory_banks))

print(f"Part 1: {redistribution_cycles}")

start_state = tuple(memory_banks)
loop_cycles = 0
while True:
    loop_cycles += 1
    to_redistribute = max(memory_banks)
    i = memory_banks.index(to_redistribute)
    memory_banks[i] = 0
    delta = max(to_redistribute // (num_banks - 1), 1)
    while to_redistribute:
        i = (i + 1) % num_banks
        amount_added = min(to_redistribute, delta)
        memory_banks[i] += amount_added
        to_redistribute -= amount_added

    if tuple(memory_banks) == start_state:
        break

print(f"Part 2: {loop_cycles}")
