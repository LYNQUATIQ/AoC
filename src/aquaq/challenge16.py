import logging
import os

import string

from collections import defaultdict

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

input_file = os.path.join(script_dir, f"inputs/ascii_art.txt")
rasters = [line.rstrip("\n") for line in open(input_file)]

input_file = os.path.join(script_dir, f"inputs/{script_name}.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
text = lines[0]

ascii_art = defaultdict(list)
leading_spaces = defaultdict(list)
trailing_spaces = defaultdict(list)
for i, c in enumerate(string.ascii_uppercase):
    for j in range(i * 6, i * 6 + 6):
        row = rasters[j].replace(" ", ".")
        ascii_art[c].append(row)
        pixel_pos = [pos for pos, char in enumerate(row) if char == "#"]
        leading_spaces[c].append(min(pixel_pos))
        trailing_spaces[c].append(len(row) - max(pixel_pos) - 1)


prior_char = text[0]
raster = ascii_art[prior_char][:]
for next_char in text[1:]:
    left_shift = [
        trailing_spaces[prior_char][i] + leading_spaces[next_char][i] for i in range(6)
    ]
    left_shift = min(left_shift)
    for i in range(6):
        first_pixel = leading_spaces[next_char][i]
        spaces = (1 + trailing_spaces[prior_char][i] + first_pixel - left_shift) * "."
        raster[i] = raster[i][: len(raster[i]) - trailing_spaces[prior_char][i]]
        raster[i] += spaces
        raster[i] += ascii_art[next_char][i][first_pixel:][:]
    prior_char = next_char

for r in raster:
    print(r)
print(sum((row.count(".") for row in raster)))
