from itertools import combinations, cycle

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
TURN = 99


class Train:
    coming_from_offsets = {
        NORTH: (0, 1),
        EAST: (-1, 0),
        SOUTH: (0, -1),
        WEST: (1, 0),
    }

    def make_turn(self, new_direction):
        if new_direction == TURN:
            turn = next(self.turn)
            new_direction = (self.coming_from + turn + 4) % 4
        self.coming_from = new_direction

    def move(self):
        dx, dy = self.coming_from_offsets[self.coming_from]
        self.x += dx
        self.y += dy

    def xy(self):
        return (self.x, self.y)

    def __init__(self, coming_from, x, y):
        self.coming_from = coming_from
        self.x = x
        self.y = y
        self.turn = cycle([-1, 0, 1])


class TrackSystem:

    track_directions = {
        # Dict of directions... Enter coming from : Leave coming from
        "-": {EAST: EAST, WEST: WEST},
        "|": {NORTH: NORTH, SOUTH: SOUTH},
        "/": {SOUTH: WEST, EAST: NORTH, WEST: SOUTH, NORTH: EAST},
        "\\": {SOUTH: EAST, EAST: SOUTH, WEST: NORTH, NORTH: WEST},
        "+": {SOUTH: TURN, EAST: TURN, WEST: TURN, NORTH: TURN},
    }

    train_pieces = {
        # Tuple: Coming from, Track piece
        "v": (NORTH, "|"),
        "^": (SOUTH, "|"),
        "<": (EAST, "-"),
        ">": (WEST, "-"),
    }

    train_coming_from = {
        NORTH: "v",
        SOUTH: "^",
        EAST: "<",
        WEST: ">",
    }

    def __init__(self, lines):
        self.train_system = {}
        self.trains = {}

        train_key = 0
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c == " ":
                    x += 1
                    continue
                try:
                    coming_from, c = self.train_pieces[c]
                    self.trains[train_key] = Train(coming_from, x, y)
                    train_key += 1
                except KeyError:
                    pass
                self.train_system[(x, y)] = c
                x += 1
            y += 1
        self.max_x = x
        self.max_y = y

    def print_system(self, tick):
        print(f"\nSystem at time {tick}")
        for y in range(self.max_y):
            for x in range(self.max_x):
                c = self.train_system.get((x, y), " ")
                for t in self.trains.values():
                    if t.xy() == (x, y):
                        c = self.train_coming_from[t.coming_from]
                        break
                print(c, end="")
            print()

    def run_trains(self):
        def train_sort_key(k):
            t = self.trains[k]
            return t.x * 1000 + t.y

        tick = 0
        finished = False
        while not finished:
            # self.print_system(tick)
            crashed_trains = set()
            for key in sorted(self.trains.keys(), key=train_sort_key):
                train = self.trains[key]
                train.move()
                for key2, train2 in self.trains.items():
                    if key != key2 and train.xy() == train2.xy():
                        print(f"Train crash at: {train.xy()}  -  tick: {tick}")
                        crashed_trains.add(key)
                        crashed_trains.add(key2)
                        break
                track_piece = self.train_system[train.xy()]
                directions = self.track_directions[track_piece]
                new_direction = directions[train.coming_from]
                train.make_turn(new_direction)
            for key in crashed_trains:
                del self.trains[key]
            finished = len(self.trains) == 1
            tick += 1

        for t in self.trains.values():
            print(f"Train at {t.x},{t.y}")


lines = [line.rstrip("\n") for line in open("2018_day13_input.txt")]
ts = TrackSystem(lines)
ts.run_trains()
print("Done")
