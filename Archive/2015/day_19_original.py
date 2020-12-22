import logging
import os

from random import shuffle


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="w",
)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


def read_replacements(lines):
    replacements = []
    for line in lines:
        tokens = line.split(" => ")
        element, replacement = tokens[0], tokens[1]
        replacements.append((element, replacement))
    return replacements


medicine = "ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF"

replacements = read_replacements(lines)


def possible_molecules(m):
    possible_molecules = set()
    for k, v in replacements:
        splits = m.split(k)
        for n in range(1, len(splits)):
            possible_molecule = ""
            for i, s in enumerate(splits):
                if i == 0:
                    possible_molecule += s
                elif i == n:
                    possible_molecule += v + s
                else:
                    possible_molecule += k + s
            possible_molecules.add(possible_molecule)
    return possible_molecules


print(f"Part 1: {len(possible_molecules(medicine))}")

target = medicine
steps = 0
while target != "e":
    last_target = target
    for k, v in replacements:
        if v not in target:
            continue
        target = target.replace(v, k, 1)
        steps += 1

    if target == last_target:
        target = medicine
        steps = 0
        shuffle(replacements)

print(f"Part 2: {steps}")