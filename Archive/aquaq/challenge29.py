import logging
import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_number = 520185742

good_numbers = 0
for n in range(input_number + 1):
    s = str(n)
    is_good = True
    for d1, d2 in zip(s[:-1], s[1:]):
        if d2 < d1:
            is_good = False
            break
    if is_good:
        good_numbers += int(is_good)

print(good_numbers)
