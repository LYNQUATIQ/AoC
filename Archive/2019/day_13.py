from collections import defaultdict

from intcode_computer import IntCodeComputer

with open("day13_input.txt") as f:
    program = f.read()

computer = IntCodeComputer(program)
score = 0
min_x, max_x, min_y, max_y = 0, 0, 0, 0


def print_screen(data, score, counter):
    pixels = {
        1: "\u2588",
        2: "*",
        3: "=",
        4: "o",
    }
    print(f"\n    SCORE: {score}           step {counter}")
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pixel = pixels.get(data[(x, y)], " ")
            print(pixel, end="")
        print()


counter = 1
paddle_input = 0
while not computer.is_terminated() and counter < 10:
    computer.run_program([paddle_input])
    output = computer.output()
    screen_data = defaultdict(list)
    print(f"length of output {len(output)}")

    while output:
        x = output.pop(0)
        y = output.pop(0)
        pixel = output.pop(0)
        if (x, y) != (-1, 0):
            screen_data[(x, y)] = pixel
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)
            if pixel == 3:
                paddle_x = x
            if pixel == 4:
                ball_x = x
        else:
            score = pixel

    print_screen(screen_data, score, counter)
    counter += 1

