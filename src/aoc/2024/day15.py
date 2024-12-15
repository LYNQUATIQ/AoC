"""https://adventofcode.com/2024/day/15"""

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 15)
example_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


WALL, BOX, ROBOT, BIG_BOX = "#", "O", "@", "[]"
UP, DOWN, LEFT, RIGHT = -1j, 1j, -1, 1
INSTRUCTIONS = {"^": UP, ">": RIGHT, "v": DOWN, "<": LEFT, "\n": 0}


def sum_box_gps(inputs: str, big_boxes: bool = False):
    grid, instructions = inputs.split("\n\n")

    walls, boxes = set(), set()
    robot_xy = None
    for y, row in enumerate(grid.split("\n")):
        x = 0
        for _, cell in enumerate(row):
            xy = complex(x, y)
            if cell == ROBOT:
                robot_xy = xy
            elif cell == WALL:
                walls.add(xy)
            elif cell == BOX:
                boxes.add(xy)
            if big_boxes:
                x += 1
                if cell == WALL:
                    walls.add(xy + RIGHT)
            x += 1

    for instruction in instructions:
        move = INSTRUCTIONS[instruction]
        if big_boxes:
            connected_boxes = {box: box + RIGHT for box in boxes}
            connected_boxes |= {v: k for k, v in connected_boxes.items()}
        xy_to_check = {robot_xy + move}
        boxes_to_move, hit_wall = set(), False
        while xy_to_check:
            if any(xy in walls for xy in xy_to_check):
                hit_wall = True
                break
            if big_boxes:
                xy_to_check = {xy for xy in xy_to_check if xy in connected_boxes}
                if move in (UP, DOWN):
                    xy_to_check |= {connected_boxes[xy] for xy in xy_to_check}
            else:
                xy_to_check = {xy for xy in xy_to_check if xy in boxes}
            boxes_to_move |= xy_to_check
            xy_to_check = {xy + move for xy in xy_to_check}

        if not hit_wall:
            robot_xy += move
            boxes_to_move &= boxes
            boxes -= boxes_to_move
            boxes |= {box + move for box in boxes_to_move}

    gps_sum = 0
    for box in boxes:
        gps_sum += int(abs(box.real) + abs(box.imag) * 100)
    return gps_sum


def solve(inputs: str):
    print(f"Part 1: {sum_box_gps(inputs)}")
    print(f"Part 2: {sum_box_gps(inputs, big_boxes=True)}\n")


solve(example_input)
solve(actual_input)
