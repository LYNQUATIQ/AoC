r2 = 10551277
r2 = 877
r3 = 1
r0 = 0

while True:
    r1 = 1
    while r1 <= r2:
        if r3 * r1 == r2:
            r0 += r3
        r1 += 1
    r3 += 1
    import pdb

    pdb.set_trace()
    if r3 > r2:
        break

print(r0)
