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

WALL, BOX, ROBOT = "#", "O", "@"
UP, DOWN, LEFT, RIGHT = -1j, 1j, -1, 1
INSTRUCTIONS = {"^": UP, ">": RIGHT, "v": DOWN, "<": LEFT, "\n": 0}


def draw_map(robot_xy, walls, boxes, width, height):
    for y in range(height):
        for x in range(width):
            xy = complex(x, y)
            if xy == robot_xy:
                print(ROBOT, end="")
            elif xy in boxes:
                print(BOX, end="")
            elif xy in walls:
                print(WALL, end="")
            else:
                print(".", end="")
        print()


def solve(inputs: str):
    grid, instructions = inputs.split("\n\n")

    walls, boxes = set(), set()
    robot_xy = None
    for y, row in enumerate(grid.split("\n")):
        for x, cell in enumerate(row):
            xy = complex(x, y)
            if cell == ROBOT:
                robot_xy = xy
            elif cell == WALL:
                walls.add(xy)
            elif cell == BOX:
                boxes.add(xy)
    assert robot_xy is not None
    width, height = x + 1, y + 1

    for instruction in instructions:
        # draw_map(robot_xy, walls, boxes, width, height)
        # print("\nMove:", instruction, f"(robot at {robot_xy})")

        move = INSTRUCTIONS[instruction]
        xy = robot_xy + move
        boxes_to_move = []
        while xy in boxes:
            boxes_to_move.append(xy)
            xy += move
        if xy in walls:
            continue
        for box in boxes_to_move[::-1]:
            boxes.remove(box)
            boxes.add(box + move)
        robot_xy += move

    gps_sum = 0
    for box in boxes:
        gps_sum += abs(box.real) + abs(box.imag) * 100
    print(f"Part 1: {int(gps_sum)}")
    print(f"Part 2: {False}\n")


solve(example_input)
solve(actual_input)
