import os

from collections import defaultdict, Counter

from intcode_computer import IntCodeComputer

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]
program = [int(i) for i in lines[0].split(",")]


class GameRenderer:
    PIXELS = {1: "\u2588", 2: "*", 3: "=", 4: "o", 0: " "}

    def __init__(self):
        self.score = 0
        self.min_x, self.max_x = 0, 0
        self.min_y, self.max_y = 0, 0
        self.paddle_x = None
        self.ball_x = None
        self.score = None
        self.screen_data = {}

    def process_ouput(self, output):
        while output:
            x, y, pixel = output.pop(0), output.pop(0), output.pop(0)
            if (x, y) == (-1, 0):
                self.score = pixel
                continue
            self.screen_data[(x, y)] = pixel
            self.min_x, self.max_x = min(x, self.min_x), max(x, self.max_x)
            self.min_y, self.max_y = min(y, self.min_y), max(y, self.max_y)
            if pixel == 3:
                self.paddle_x = x
            if pixel == 4:
                self.ball_x = x

    def print_screen(self, counter):
        print(f"\n    SCORE: {self.score}           step {counter}")
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                pixel = self.PIXELS[self.screen_data.get((x, y), 0)]
                print(pixel, end="")
            print()


computer = IntCodeComputer(program)
game = GameRenderer()
computer.run_program()
game.process_ouput(computer.output())
print(f"Part 1: {Counter(game.screen_data.values())[2]}")

computer = IntCodeComputer(program, {0: 2})
game = GameRenderer()
counter = 0
paddle_input = 0
while not computer.is_terminated():
    computer.run_program([paddle_input])
    game.process_ouput(computer.output())
    paddle_input = (game.ball_x > game.paddle_x) - (game.ball_x < game.paddle_x)
    counter += 1

print(f"Part 2: {game.score}")
