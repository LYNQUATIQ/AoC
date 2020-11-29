import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
directions = lines[0]


class Dice:
    def __init__(self, front, left, top):
        self.front = front
        self.left = left
        self.top = top

    def __repr__(self):
        return f"F{self.front} L{self.left} T{self.top}"

    def rotate(self, direction):
        if direction == "U":
            front = 7 - self.top
            left = self.left
            top = self.front
        if direction == "D":
            front = self.top
            left = self.left
            top = 7 - self.front
        if direction == "L":
            front = 7 - self.left
            left = self.front
            top = self.top
        if direction == "R":
            front = self.left
            left = 7 - self.front
            top = self.top
        self.front = front
        self.left = left
        self.top = top
        return self.front


d1 = Dice(1, 2, 3)
d2 = Dice(1, 3, 2)

output = 0
for i, direction in enumerate(directions):
    print(f"  D1({d1})  D2({d2})  ->{direction}->  ", end="")
    match = ""
    if d1.rotate(direction) == d2.rotate(direction):
        output += i
        match = "MATCH!"
    print(f"D1({d1})  D2({d2})  {match}")

print(f"ANSWER: {output}")
