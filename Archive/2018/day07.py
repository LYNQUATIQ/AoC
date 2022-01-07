"""https://adventofcode.com/2018/day/7"""
from collections import defaultdict
import os
import re


with open(os.path.join(os.path.dirname(__file__), f"inputs/day07_input.txt")) as f:
    actual_input = f.read()

sample_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""


def solve(inputs, num_workers=2, step_duration=0):
    dependencies, steps = defaultdict(set), set()
    for line in inputs.splitlines():
        a, b = re.findall(r"[A-Z]", line[1:])
        dependencies[b].add(a)
        steps.update((a, b))

    to_finish, completed = set(steps), []
    while to_finish:
        next_step = sorted(
            s for s in to_finish if all(d in completed for d in dependencies[s])
        )[0]
        completed.append(next_step)
        to_finish.remove(next_step)
    print(f"Part 1: {''.join(completed)}")

    elapsed_time = 0
    workers = set(range(num_workers))
    working_on, completed, pending = {}, {}, set(steps)
    while completed != steps:
        finished_workers = {w for w in working_on if working_on[w][1] == elapsed_time}
        for worker in finished_workers:
            completed.add(working_on.pop(worker)[0])

        free_workers = {w for w in workers if w not in working_on}
        jobs_to_do = sorted(
            [s for s in pending if all(d in completed for d in dependencies[s])],
            reverse=True,
        )
        while free_workers and jobs_to_do:
            next_step, next_worker = jobs_to_do.pop(), free_workers.pop()
            pending.remove(next_step)
            working_on[next_worker] = (
                next_step,
                elapsed_time + step_duration + ord(next_step) - ord("A") + 1,
            )
        elapsed_time += 1

    print(f"Part 2: {elapsed_time-1}\n")


solve(sample_input)
solve(actual_input, 5, 60)
