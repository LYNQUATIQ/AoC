import os

from collections import Counter

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
IMAGE_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT
ASCII_PIXEL = "\u2588"

image = [line.rstrip("\n") for line in open(input_file)][0]
layers = [image[i : i + IMAGE_SIZE] for i in range(0, len(image), IMAGE_SIZE)]

part1, fewest_zeroes = None, float("inf")
for layer in layers:
    counts = Counter(layer)
    if int(counts["0"]) < fewest_zeroes:
        fewest_zeroes = int(counts["0"])
        part1 = int(counts["1"]) * int(counts["2"])
print(f"Part 1: {part1}")

print("Part 2:")
print(ASCII_PIXEL * (IMAGE_WIDTH + 1))
for y in range(IMAGE_HEIGHT):
    print(ASCII_PIXEL, end="")
    for x in range(IMAGE_WIDTH):
        i = y * IMAGE_WIDTH + x
        for layer in layers:
            if layer[i] in "01":
                print(ASCII_PIXEL if layer[i] == "0" else " ", end=""),
                break
    print("")
print(ASCII_PIXEL * (IMAGE_WIDTH + 1))
