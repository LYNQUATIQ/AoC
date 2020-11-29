import logging
import os

import bisect
from collections import Counter

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)

to_decode = "1000010010001100110001010011011101101100110000110011010111001000110011001101110101101011001001100001101100110000101100011001000101011011101111101100010011011111110010010101011101000011011011101101010110111011011011001111100111111010010111111100110101111010101111000110110011110011110001010010111110110111011001100110101010101101110000111000011010111111010111111000100101011101111101001110000100101110000111111010111011001011001001010111100110101111000110011000010010100101111110011111101111000111100011011101001101111010001101100100010100110111001100001011000110010011010001100000011100110111001100001100110111110101101100010101101100110111000110101111101100010011011101011010110010011010011011000111000110101111101011001"
input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
chars = lines[0]

counts = Counter(chars)


class Token:
    @classmethod
    def new_token(cls, left, right):
        new_token = cls(left.token + right.token, left.weight + right.weight)
        new_token.left = left
        new_token.right = right
        return new_token

    def leaf_node(self):
        return len(self.token) == 1

    def __init__(self, token: str, weight: int):
        self.token = token
        self.weight = weight
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.weight == other.weight:
            return self.token < other.token
        return self.weight < other.weight

    def __repr__(self):
        return f"{self.token}:{self.weight}"


tokens = [Token(token, weight) for token, weight in counts.items()]
tokens.sort()
while True:
    left = tokens[0]
    right = tokens[1]
    tokens = tokens[2:]
    token = Token.new_token(left, right)
    if len(tokens) == 0:
        break
    lo, hi = 0, len(tokens)
    while lo < hi:
        mid = (lo + hi) // 2
        if token.weight < tokens[mid].weight:
            hi = mid
        else:
            lo = mid + 1
    tokens.insert(lo, token)

base_token = token
assert len(chars) == base_token.weight

output = ""
i = 0
while i < len(to_decode):
    if to_decode[i] == "1":
        token = token.right
    else:
        token = token.left
    if token.leaf_node():
        output += token.token
        token = base_token
    i += 1

print(output)