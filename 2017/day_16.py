import logging
import os

from grid_system import XY


script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_16.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/2017_day_16_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]
assert len(lines) == 1
dance_moves = lines[0].split(",")

def perform_dance(line_up, dance_moves):
    line_up = [p for p in line_up]

    for dance_move in dance_moves:
        move = dance_move[0]
        step = dance_move[1:]

        if move == "s":
            split = int(step) * -1
            a = line_up[split:] 
            b = line_up[0:split]
            line_up = a + b    
            continue

        if move == "x":
            a, b = (int(x) for x in step.split("/"))
            line_up[a], line_up[b] = line_up[b], line_up[a]       
            continue

        if move == "p":
            a, b = (step.split("/"))
            a = line_up.index(a)
            b = line_up.index(b)
            line_up[a], line_up[b] = line_up[b], line_up[a]    
            continue

    return "".join(line_up)

print(f"Part 1: {perform_dance('abcdefghijklmnop', dance_moves)}")

iteration = 0
line_up = "abcdefghijklmnop"
iterations = { 0: line_up }
while True:
    iteration += 1
    line_up = perform_dance(line_up, dance_moves)
    if line_up == "abcdefghijklmnop":
        break
    iterations[iteration] = line_up

print(f"Part 2: {iterations[1000000000 % iteration]}")
