import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day13_input.txt")) as f:
    actual_input = f.read()

sample_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def solve(inputs):
    dots, folds = map(lambda x: x.splitlines(), inputs.split("\n\n"))
    dots = {map(int, xy.split(",")) for xy in dots}
    folds = map(lambda f: (f[0], int(f[1])), (f.split()[-1].split("=") for f in folds))

    for step, (xy, fold_line) in enumerate(folds):
        dots = {
            (
                2 * fold_line - x if xy == "x" and x >= fold_line else x,
                2 * fold_line - y if xy == "y" and y >= fold_line else y,
            )
            for x, y in dots
        }
        if step == 0:
            print(f"\nPart 1: {len(dots)}")

    print("Part 2: ")
    max_x, max_y = max(xy[0] for xy in dots), max(xy[1] for xy in dots)
    for y in range(max_y + 1):
        print("".join("\u2588" if (x, y) in dots else " " for x in range(max_x + 1)))


solve(sample_input)
solve(actual_input)
