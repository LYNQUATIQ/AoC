import logging
import os

import re
import string

from collections import Counter, defaultdict


script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]

log_file = os.path.join(script_dir, f"logs/{script_name}.log")
logging.basicConfig(level=logging.WARNING, filename=log_file, filemode='w',)

input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip('\n') for line in open(input_file)]


class Room:
    def __init__(self, encrypted_name, sector_id, checksum):
        self.encrypted_name = encrypted_name
        self.sector_id = int(sector_id)
        self.checksum = checksum

    def decrypted_name(self):
        name = ""
        for c in self.encrypted_name:
            if c == "-":
                name += " "
                continue
            name += chr(ord("a") + ((ord(c) - ord("a")) + self.sector_id) % 26)
        return name

    def is_valid(self):
        letters = [c for c in self.encrypted_name if c != "-"]
        letter_counts = defaultdict(list)
        for letter, count in Counter(letters).items():
            letter_counts[count].append(letter)
        checksum = ""
        for count in sorted(letter_counts.keys(), reverse=True):
            for l in sorted(letter_counts[count]):
                checksum += l
                if len(checksum) == 5:
                    return checksum == self.checksum

        raise NotImplementedError


regex = re.compile(r"^(?P<encrypted_name>[a-z\-]+)-(?P<sector_id>\d+)\[(?P<checksum>[a-z]{5})\]$")

rooms = {}
for line in lines:
    room = Room(**regex.match(line).groupdict())
    rooms[room.encrypted_name] = room

sector_id_sum = 0
for room in rooms.values():
    if room.is_valid():
        sector_id_sum += room.sector_id
        
print(f"Part 1: {sector_id_sum}")

for room in rooms.values():
    if room.is_valid():
        room_name = room.decrypted_name()
        if all([w in room_name for w in ["north", "pole"]]):
            print(f"Part 2: {room.sector_id}   ({room_name})")
            break