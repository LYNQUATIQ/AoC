import logging
import os


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="w",
)

puzzle_input = 29000000


def get_divisors(n):
    divisors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n / i)
    return divisors


house = 100000
while True:
    if sum(get_divisors(house)) * 10 >= puzzle_input:
        break
    house += 1

print(f"Part 1: {house}")

house = 100000
while True:
    if sum([i for i in get_divisors(house) if 50 * i >= house]) * 11 >= puzzle_input:
        break
    house += 1

print(f"Part 2: {house}")
