import logging
import os

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]


def longest_repeating_substring(string):
    string_count = defaultdict(int)

    n = len(string)

    # banana
    # 012345 6

    for i in range(n):
        for j in range(i + 1, n):
            sub_string = string[i:j]
            l = len(sub_string)
            k = i
            while k + l <= n and string[k : k + l] == sub_string:
                string_count[(i, j)] += 1
                k += l

    i, j = max(string_count, key=string_count.get)
    return string[i:j], string_count[(i, j)]


answer = 0
for line in lines:
    _, n = longest_repeating_substring(line)
    answer += n

print(answer)
