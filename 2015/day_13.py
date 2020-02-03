import logging
import os

from itertools import permutations

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

participants = set()
happiness_delta = {}

for line in lines:
    tokens = line.split(" ")
    a = tokens[0]
    delta = {"gain": +1, "lose": -1}[tokens[2]] * int(tokens[3])
    b  = tokens[10][:-1]
    participants.add(a)
    happiness_delta[(a, b)] = delta

participants = sorted(list(participants))

def total_happiness(first_participant, other_participants):
    n = len(other_participants)
    arrangements = permutations(other_participants)
    max_happiness = 0
    for seating in arrangements:
        happiness = 0
        for i in range(n - 1):
            happiness += happiness_delta.get((seating[i], seating[i+1]), 0)
            happiness += happiness_delta.get((seating[n - i - 1], seating[n - i - 2]), 0)
        happiness += happiness_delta.get((first_participant, seating[0]), 0)
        happiness += happiness_delta.get((first_participant, seating[-1]), 0)
        happiness += happiness_delta.get((seating[0], first_participant), 0)
        happiness += happiness_delta.get((seating[-1], first_participant), 0)
        max_happiness = max(happiness, max_happiness)
    return max_happiness


print(f"Part 1: {total_happiness(participants[0], participants[1:])}")
print(f"Part 2: {total_happiness('me', participants)}")
     
