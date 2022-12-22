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

TURN_ANTICLOCKWISE = {EAST: NORTH, NORTH: WEST, WEST: SOUTH, SOUTH: EAST}
TURN_CLOCKWISE = {EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST}
TURN = {"L": TURN_ANTICLOCKWISE, "R": TURN_CLOCKWISE}

# Which face (and the side on the face) is connected to the E,S,W,N of this face
EXAMPLE_LINKS = (
    ((0, EAST), (3, SOUTH), (0, WEST), (4, NORTH)),
    ((2, EAST), (1, SOUTH), (3, WEST), (1, NORTH)),
    ((3, EAST), (2, SOUTH), (1, WEST), (2, NORTH)),
    ((1, EAST), (4, SOUTH), (2, WEST), (0, NORTH)),
    ((5, EAST), (0, SOUTH), (5, WEST), (3, NORTH)),
    ((4, EAST), (5, SOUTH), (4, WEST), (5, NORTH)),
)
EXAMPLE_CUBE_LINKS = (
    ((5, WEST), (3, SOUTH), (2, SOUTH), (1, SOUTH)),
    ((2, EAST), (4, NORTH), (5, NORTH), (0, SOUTH)),
    ((3, EAST), (4, EAST), (1, WEST), (0, EAST)),
    ((5, SOUTH), (4, SOUTH), (2, WEST), (0, NORTH)),
    ((5, EAST), (1, NORTH), (2, NORTH), (3, NORTH)),
    ((0, WEST), (1, EAST), (4, WEST), (3, WEST)),
)
ACTUAL_LINKS = (
    ((1, EAST), (2, SOUTH), (1, WEST), (4, NORTH)),
    ((0, EAST), (1, SOUTH), (0, WEST), (1, NORTH)),
    ((2, EAST), (4, SOUTH), (2, WEST), (0, NORTH)),
    ((4, EAST), (5, SOUTH), (4, WEST), (5, NORTH)),
    ((3, EAST), (0, SOUTH), (3, WEST), (2, NORTH)),
    ((5, EAST), (3, SOUTH), (5, WEST), (3, NORTH)),
)
ACTUAL_CUBE_LINKS = (
    ((1, EAST), (2, SOUTH), (3, EAST), (5, EAST)),
    ((4, WEST), (2, WEST), (0, WEST), (5, NORTH)),
    ((1, NORTH), (4, SOUTH), (3, SOUTH), (0, NORTH)),
    ((4, EAST), (5, SOUTH), (0, EAST), (2, EAST)),
    ((1, WEST), (5, WEST), (3, WEST), (2, NORTH)),
    ((4, NORTH), (1, SOUTH), (0, SOUTH), (3, NORTH)),
)


def navigate_path(
    instructions: str, faces: list[list[str]], face_size: int, is_cube: bool = False
) -> int:
    links = EXAMPLE_LINKS if face_size == 4 else ACTUAL_LINKS
    if is_cube:
        links = EXAMPLE_CUBE_LINKS if face_size == 4 else ACTUAL_CUBE_LINKS

    current_face, x, y, moving = 0, 0, 0, EAST
    ptr = 0
    finished = False
    while not finished:

        # Check if we're turning
        if instructions[ptr] in "LR":
            moving = TURN[instructions[ptr]][moving]
            ptr += 1
            continue

        # If not determine the steps we're moving
        steps = 0
        while instructions[ptr].isdigit():
            steps = steps * 10 + int(instructions[ptr])
            ptr += 1
            if ptr == len(instructions):
                finished = True
            if finished or not instructions[ptr].isdigit():
                break

        # Keep taking steps (navigating over face edges) until we're done or hit a wall
        while steps:
            next_face, next_direction = current_face, moving
            if moving == EAST:
                next_x, next_y = x + 1, y
                if next_x >= face_size:
                    next_face, next_direction = links[current_face][moving]
                    next_x, next_y = {
                        EAST: (0, next_y),
                        SOUTH: (face_size - next_y - 1, 0),
                        WEST: (face_size - 1, face_size - next_y - 1),
                        NORTH: (next_y, face_size - 1),
                    }[next_direction]
            elif moving == SOUTH:
                next_x, next_y = x, y + 1
                if next_y >= face_size:
                    next_face, next_direction = links[current_face][moving]
                    next_x, next_y = {
                        EAST: (0, face_size - next_x - 1),
                        SOUTH: (next_x, 0),
                        WEST: (face_size - 1, next_x),
                        NORTH: (face_size - next_x - 1, face_size - 1),
                    }[next_direction]
            elif moving == WEST:
                next_x, next_y = x - 1, y
                if next_x < 0:
                    next_face, next_direction = links[current_face][moving]
                    next_x, next_y = {
                        EAST: (0, face_size - next_y - 1),
                        SOUTH: (next_y, 0),
                        WEST: (face_size - 1, next_y),
                        NORTH: (face_size - next_y - 1, face_size - 1),
                    }[next_direction]
            elif moving == NORTH:
                next_x, next_y = x, y - 1
                if next_y < 0:
                    next_face, next_direction = links[current_face][moving]
                    next_x, next_y = {
                        EAST: (0, next_x),
                        SOUTH: (face_size - next_x - 1, 0),
                        WEST: (face_size - 1, face_size - next_x - 1),
                        NORTH: (next_x, face_size - 1),
                    }[next_direction]

            if faces[next_face][next_y][next_x] == "#":
                break
            current_face, x, y, moving = next_face, next_x, next_y, next_direction
            steps -= 1

    layout = EXAMPLE_LAYOUT if face_size == 4 else ACTUAL_LAYOUT
    offset_x, offset_y = layout[current_face]
    x, y = offset_x * face_size + x, offset_y * face_size + y
    return 1000 * (y + 1) + 4 * (x + 1) + moving


def solve(inputs: str, face_size: int) -> None:
    map_data, instructions = inputs.split("\n\n")
    map_rows = [row for row in map_data.splitlines()]
    faces = []
    for (offset_x, offset_y) in EXAMPLE_LAYOUT if face_size == 4 else ACTUAL_LAYOUT:
        x, y = offset_x * face_size, offset_y * face_size
        faces.append([map_rows[y][x : x + face_size] for y in range(y, y + face_size)])

    print(f"Part 1: {navigate_path(instructions, faces, face_size)}")
    print(f"Part 2: {navigate_path(instructions, faces, face_size, is_cube=True)}\n")


solve(sample_input, 4)
solve(actual_input, 50)
