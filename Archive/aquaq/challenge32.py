import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

close_params = {"}": "{", "]": "[", ")": "("}
answer = 0
for line in lines:
    open_params = ["*"]
    good = True
    for c in line:
        if c in close_params:
            if open_params.pop() != close_params[c]:
                good = False
                break
        if c in "{[(":
            open_params.append(c)
    if open_params != ["*"]:
        good = False
    if good:
        answer += 1

print(answer)
