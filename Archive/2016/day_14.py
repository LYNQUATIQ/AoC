import logging
import os

import hashlib
import re

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

match3 = re.compile(r"(\w)\1{2,}")
salt = "ihaygndm"

def get_hash_keys(salt, stretches=0):
    hashes = {}

    def get_hash(key):
        try:
            hash_value = hashes[key]
        except KeyError:
            hash_value = hashlib.md5(f"{salt}{key}".encode()).hexdigest()
            for _ in range(stretches):
                hash_value = hashlib.md5(hash_value.encode()).hexdigest()
            hashes[key] = hash_value
        return hash_value

    index_value = 0
    found_keys = []
    while len(found_keys) < 64:
        hash_value = get_hash(index_value)
        match = match3.search(hash_value)
        if match:
            match_digit = match[0][0]
            match5 = match_digit * 5
            for i in range(1, 1001):
                if match5 in get_hash(index_value + i):
                    found_keys.append(hash_value)
                    break
        index_value += 1

    return index_value - 1

print(f"Part 1: {get_hash_keys(salt)}")

print(f"Part 2: {get_hash_keys(salt, 2016)}")

