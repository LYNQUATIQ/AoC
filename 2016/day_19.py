import logging
import os
import time

from collections import deque

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)


def white_elephant(num_elves):
    circle = { n + 1 : ((n + 1) % num_elves) + 1 for n in range(num_elves) }
    current_elf = 1
    while num_elves > 1:
        circle[current_elf] = circle[circle[current_elf]]
        current_elf = circle[current_elf]
        num_elves -= 1
    return current_elf

print(f"Part 1: {white_elephant(3014387)}")

def white_elephant2(num_elves):
    total_elves = num_elves
    circle = { n : ((n + 1) % num_elves) for n in range(num_elves) }
    full_circle = { k: "e" for k in circle.keys() }
    current_elf = 0
    last_removed = None
    total_steps = 0
    deltas = ""
    removed = []
    while num_elves > 1:
        last_elf = current_elf
        elf = current_elf
        for _ in range(num_elves // 2 - 1):
            elf = circle[elf]
        to_remove = circle[elf]
        removed.append(str(to_remove))
        full_circle[to_remove] = "-"
        circle[elf] = circle[circle[elf]]
        current_elf = circle[current_elf]
        num_elves -= 1
        if last_removed is not None:
            delta = (to_remove - last_removed)%total_elves
            total_steps += delta
            deltas += f"{delta:>3}"
        last_removed = to_remove
    last_elf = current_elf + 1
    return last_elf


def white_elephant2_fast(num_elves):
    circle = set(range(num_elves))
    step_size = 1
    mid_point = num_elves // 2 
    to_remove = mid_point
    double_step = not bool(num_elves % 2)  
    removed = []
    while len(circle) > 1:
        done = False
        while len(circle) > 1 and not done:
            circle.remove(to_remove)
            last_removed = to_remove
            removed.append(str(last_removed))
            double_step = not double_step
            to_remove = (to_remove + (step_size + double_step * step_size)) % num_elves
            done = last_removed < mid_point and to_remove >= mid_point
        step_size *= 3
        to_remove = last_removed
        for _ in range(1 + double_step):
            while True:
                to_remove = (to_remove + 1) % num_elves
                if to_remove in circle:
                    break
    last_elf = circle.pop() + 1
    return last_elf

print(f"Part 2: {white_elephant2_fast(3014387)}")

def solve_parttwo(num_elves):
    left = deque()
    right = deque()
    mid_point = (num_elves // 2) + 1
    for i in range(1, num_elves + 1):
        if i < mid_point:
            left.append(i)
        else:
            right.appendleft(i)

    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()
        # rotate
        right.appendleft(left.popleft())
        left.append(right.pop())
    return left[0] or right[0]

print(f"Part 2: {solve_parttwo(3014387)}")
print(f"{time.time()-t}\n")
