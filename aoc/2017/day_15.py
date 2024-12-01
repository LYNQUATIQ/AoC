import logging
import os
import time

script_dir = os.path.dirname(__file__)
log_file = os.path.join(script_dir, "logs/2017_day_15.log")
logging.basicConfig(
    level=logging.WARNING,
    filename=log_file,
    filemode="w",
)


class Generator:
    MODULO = 2147483647

    def __init__(self, initial, factor, multiple_check=1):
        self.value = initial
        self.factor = factor
        self.multiple_check = multiple_check

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            self.value = (self.value * self.factor) % self.MODULO
            if self.value % self.multiple_check == 0:
                return self.value


a, b = 634, 301

generator_a = Generator(a, 16807)
generator_b = Generator(b, 48271)
matches = 0
t = time.time()
for _ in range(40000000):
    if next(generator_a) & 0xFFFF == next(generator_b) & 0xFFFF:
        matches += 1
print(f"Part 1: {matches}   ({time.time()-t}s)")

generator_a = Generator(a, 16807, 4)
generator_b = Generator(b, 48271, 8)
matches = 0
t = time.time()
for _ in range(5000000):
    if next(generator_a) & 0xFFFF == next(generator_b) & 0xFFFF:
        matches += 1
print(f"Part 2: {matches}   ({time.time()-t}s)")
