import os

with open(os.path.join(os.path.dirname(__file__), f"inputs/upping_the_ante.txt")) as f:
    waves = f.read()


bits = []
for wave in (list(map(int, line.split(","))) for line in waves.splitlines()):
    boundary_crosses = []
    for b1, b2 in zip(wave[:-1], wave[1:]):
        boundary_crosses.append((b1 > 0) != (b2 > 0))
    bits.append(str(int(sum(boundary_crosses) // 10)))

bits8 = zip(*[bits[i::8] for i in range(8)])
print("".join(chr(int("".join(byte[1:-2]), 3)) for byte in bits8))
