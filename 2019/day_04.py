import re

LOWER, UPPER = 402328, 864247

part1, part2 = 0, 0
for password in [str(n) for n in range(LOWER, UPPER + 1)]:
    if any(d1 > d2 for d1, d2 in zip(password[:-1], password[1:])):
        continue
    double_digits = set(re.findall(r"(\d)\1{1}", password))
    if not double_digits:
        continue
    part1 += 1
    triple_digits = set(re.findall(r"(\d)\1{2}", password))
    if double_digits - triple_digits:
        part2 += 1


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
