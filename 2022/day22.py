"""https://adventofcode.com/2022/day/22"""
import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/day22_input.txt")) as f:
    actual_input = f.read()


sample_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


EXAMPLE_LAYOUT = ((2, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2))
ACTUAL_LAYOUT = ((1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (0, 3))

EAST, SOUTH, WEST, NORTH = 0, 1, 2, 3
# Which patch (and the side on the patch) is connected to the E,S,W,N of this patch
EXAMPLE_PART_1_LINKS = (
    ((0, EAST), (3, SOUTH), (0, WEST), (4, NORTH)),
    ((2, EAST), (1, SOUTH), (3, WEST), (1, NORTH)),
    ((3, EAST), (2, SOUTH), (1, WEST), (2, NORTH)),
    ((1, EAST), (4, SOUTH), (2, WEST), (0, NORTH)),
    ((5, EAST), (0, SOUTH), (5, WEST), (3, NORTH)),
    ((4, EAST), (5, SOUTH), (4, WEST), (5, NORTH)),
)
EXAMPLE_PART_2_LINKS = (
    ((5, WEST), (3, SOUTH), (2, SOUTH), (1, SOUTH)),
    ((2, EAST), (4, NORTH), (5, NORTH), (0, SOUTH)),
    ((3, EAST), (4, EAST), (1, WEST), (0, EAST)),
    ((5, SOUTH), (4, SOUTH), (2, WEST), (0, NORTH)),
    ((5, EAST), (1, NORTH), (2, NORTH), (3, NORTH)),
    ((0, WEST), (1, EAST), (4, WEST), (3, WEST)),
)
ACTUAL_PART_1_LINKS = (
    ((1, EAST), (2, SOUTH), (1, WEST), (4, NORTH)),
    ((0, EAST), (1, SOUTH), (0, WEST), (1, NORTH)),
    ((2, EAST), (4, SOUTH), (2, WEST), (0, NORTH)),
    ((4, EAST), (5, SOUTH), (4, WEST), (5, NORTH)),
    ((3, EAST), (0, SOUTH), (3, WEST), (2, NORTH)),
    ((5, EAST), (3, SOUTH), (5, WEST), (3, NORTH)),
)
ACTUAL_PART_2_LINKS = (
    ((1, EAST), (2, SOUTH), (3, EAST), (5, EAST)),
    ((4, WEST), (2, WEST), (0, WEST), (5, NORTH)),
    ((1, NORTH), (4, SOUTH), (3, SOUTH), (0, NORTH)),
    ((4, EAST), (5, SOUTH), (0, EAST), (2, EAST)),
    ((1, WEST), (5, WEST), (3, WEST), (2, NORTH)),
    ((4, NORTH), (1, SOUTH), (0, SOUTH), (3, NORTH)),
)


FACING = {EAST: 0, SOUTH: 1, WEST: 2, NORTH: 3}
TURN_ANTICLOCKWISE = {EAST: NORTH, NORTH: WEST, WEST: SOUTH, SOUTH: EAST}
TURN_CLOCKWISE = {EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST}
TURN = {"L": TURN_ANTICLOCKWISE, "R": TURN_CLOCKWISE}

# DX_DY = {EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0), NORTH: (0, -1)}
WALL = "#"


def navigate_path(
    instructions: str, patches: list[list[str]], patch_size: int, is_part2: bool
) -> int:
    layout = EXAMPLE_LAYOUT if patch_size == 4 else ACTUAL_LAYOUT
    links = {
        False: EXAMPLE_PART_1_LINKS if patch_size == 4 else ACTUAL_PART_1_LINKS,
        True: EXAMPLE_PART_2_LINKS if patch_size == 4 else ACTUAL_PART_2_LINKS,
    }[is_part2]

    current_patch, x, y, facing = 0, 0, 0, EAST
    ptr = 0
    finished = False
    while not finished:
        if instructions[ptr] in "LR":
            facing = TURN[instructions[ptr]][facing]
            ptr += 1
            continue
        steps = 0
        while instructions[ptr].isdigit():
            steps = steps * 10 + int(instructions[ptr])
            ptr += 1
            if ptr == len(instructions):
                finished = True
            if finished or not instructions[ptr].isdigit():
                break
        while steps:
            next_patch, next_facing = current_patch, facing
            if facing == EAST:
                next_x, next_y = x + 1, y
                if next_x == patch_size:
                    next_patch, next_facing = links[current_patch][EAST]
                    next_x, next_y = {
                        EAST: (0, next_y),
                        SOUTH: (patch_size - next_y - 1, 0),
                        WEST: (patch_size - 1, patch_size - next_y - 1),
                        NORTH: (next_y, patch_size - 1),
                    }[next_facing]
            elif facing == SOUTH:
                next_x, next_y = x, y + 1
                if next_y == patch_size:
                    next_patch, next_facing = links[current_patch][SOUTH]
                    next_x, next_y = {
                        EAST: (0, patch_size - next_x - 1),
                        SOUTH: (next_x, 0),
                        WEST: (patch_size - 1, next_x),
                        NORTH: (patch_size - next_x - 1, patch_size - 1),
                    }[next_facing]
            elif facing == WEST:
                next_x, next_y = x - 1, y
                if next_x == -1:
                    next_patch, next_facing = links[current_patch][WEST]
                    next_x, next_y = {
                        EAST: (0, patch_size - next_y - 1),
                        SOUTH: (next_y, 0),
                        WEST: (patch_size - 1, next_y),
                        NORTH: (patch_size - next_y - 1, patch_size - 1),
                    }[next_facing]
            elif facing == NORTH:
                next_x, next_y = x, y - 1
                if next_y == -1:
                    next_patch, next_facing = links[current_patch][NORTH]
                    next_x, next_y = {
                        EAST: (0, next_x),
                        SOUTH: (patch_size - next_x - 1, 0),
                        WEST: (patch_size - 1, patch_size - next_x - 1),
                        NORTH: (next_x, patch_size - 1),
                    }[next_facing]

            if patches[next_patch][next_y][next_x] == WALL:
                break
            current_patch, x, y, facing = next_patch, next_x, next_y, next_facing
            steps -= 1

            # offset_x, offset_y = layout[current_patch]
            # print((offset_x * patch_size + x, offset_y * patch_size + y), end="")
            # print(f"    (Patch: {current_patch} - {x},{y})")

    offset_x, offset_y = layout[current_patch]
    x, y = offset_x * patch_size + x, offset_y * patch_size + y
    # print(x, y, facing)
    return 1000 * (y + 1) + 4 * (x + 1) + facing


def solve(inputs: str, patch_size: int) -> None:
    map_data, instructions = inputs.split("\n\n")
    input_data = [row for row in map_data.splitlines()]
    patches = []
    for (offset_x, offset_y) in EXAMPLE_LAYOUT if patch_size == 4 else ACTUAL_LAYOUT:
        offset_x *= patch_size
        offset_y *= patch_size
        patch = []
        for y in range(offset_y, offset_y + patch_size):
            patch.append(input_data[y][offset_x : offset_x + patch_size])
        patches.append(patch)

    print(f"Part 1: {navigate_path(instructions, patches, patch_size, is_part2=False)}")
    print(f"Part 2: {navigate_path(instructions, patches, patch_size, is_part2=True)}")
    print()


solve(sample_input, 4)
solve(actual_input, 50)
