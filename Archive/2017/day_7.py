import logging
import os
import re

from collections import Counter

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_7.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, "inputs/2017_day_7_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]

class Program:
    def __init__(self, name):
        self.name = name
        self.weight = None
        self.parent = None
        self.children = []
        self._childrens_weights = None

    def assign_weight(self, weight):
        self.weight = weight

    def assign_parent(self, parent):
        self.parent = parent

    def assign_children(self, children):
        self.children = children

    @property
    def childrens_weights(self):
        if self._childrens_weights is None:
            self._childrens_weights = [programs[c].total_weight() for c in self.children]
        return self._childrens_weights

    def total_weight(self):
        return self.weight + sum(self.childrens_weights)

    def balanced(self):
        return len(set(self.childrens_weights)) == 1

programs = {}

for line in lines:
    pattern = re.compile(r"^(?P<name>[a-z]+) \((?P<weight>\d+)\)( -> (?P<children>[a-z, ]*))?$")
    for line in lines:
        params = pattern.match(line).groupdict()
        name = params["name"]
        program = Program(params["name"])
        program = programs.get(name, Program(name))
        programs[name] = program
        program.assign_weight(int(params["weight"]))
        programs[program.name] = program
        children = params["children"]
        if children is not None:
            children = children.split(", ")
            program.assign_children(children)
            for child in children:
                child_program = programs.get(child, Program(child))
                programs[child] = child_program
                child_program.assign_parent(program)

for p in programs.values():
    if p.parent is None:
        root = p
        break

print(f"Part 1: {root.name}")

spacer = ""
program = root
incorrect_delta = None
while True:
    print(f"{spacer}{program.name} ({program.weight}/{program.total_weight()})")
    spacer += "  "
    weights_children = {}
    for child in program.children:
        p = programs[child]
        print(f"{spacer}{p.name} ({p.total_weight()})")
        weights_children[p.total_weight()] = p
    print()

    weight_counts = Counter(program.childrens_weights)
    if(len(weight_counts) == 1):
        break
    if incorrect_delta is None:
        correct = None
        incorrect = None
        for w, c in weight_counts.items():
            if c == 1:
                incorrect = w
            else:
                correct = w
        incorrect_delta = incorrect - correct
    if incorrect_delta > 0:
        incorrect_weight = max(weight_counts.keys())
    else:
        incorrect_weight = min(weight_counts.keys())

    program = weights_children[incorrect_weight]

print(f"Part 2: {program.weight - incorrect_delta}")