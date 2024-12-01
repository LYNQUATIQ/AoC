import hashlib


actual_input = "ckczppom"


def get_answer(secret_key, num_zeroes):
    answer = 0
    while True:
        input_str = f"{secret_key}{answer}"
        result = hashlib.md5(input_str.encode())
        hex_output = result.hexdigest()
        if hex_output[0:num_zeroes] == "0" * num_zeroes:
            break
        answer += 1
    return answer


def solve(inputs):
    print(f"Part 1: {get_answer(inputs, 5)}")
    print(f"Part 2: {get_answer(inputs, 6)}\n")


solve(actual_input)
