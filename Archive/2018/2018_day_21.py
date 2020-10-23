def calculate_day_21_answers():
    r3 = 0  # 5
    possible_answers = set()
    while True:
        r2 = r3 | 0x10000  # 6
        r3 = 0x10C597  # 7

        while True:
            r3 += r2 & 0xFF  # 9  Bottom 8 bits of r2
            r3 &= 0xFFFFFF  # 10   Bottom 24 bits of r3
            r3 *= 0x1016B  # 11
            r3 = r3 & 0xFFFFFF  # 12   Bottom 24 bits of r3

            if r2 < 256:  # 13
                if not possible_answers:
                    print(f"Part 1 = {r3}")
                if r3 in possible_answers:
                    print(f"Part 2 = {last_unseen_answer}")
                    return
                last_unseen_answer = r3
                possible_answers.add(r3)
                break  # Back to outer loop (bori 3 65536 2)
            else:
                r2 = r2 // 256


calculate_day_21_answers()
