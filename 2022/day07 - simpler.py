"""https://adventofcode.com/2022/day/7"""
from __future__ import annotations

import os

from typing import Optional

with open(os.path.join(os.path.dirname(__file__), f"inputs/day07_input.txt")) as f:
    actual_input = f.read()


sample_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class Directory:
    def __init__(self, parent: Optional[Directory] = None) -> None:
        self.parent = parent or self
        self.sub_directories: dict[str, Directory] = {}
        self.file_size = 0

    @property
    def size(self) -> int:
        return sum(x.size for x in self.sub_directories.values()) + self.file_size


def solve(inputs: str) -> None:

    root = Directory()
    all_directories: set[Directory] = {root}

    current = root
    for command in inputs.split("$ "):

        if command.startswith("cd"):
            _, target = command.split()
            if target == "/":
                current = root
            elif target == "..":
                current = current.parent
            else:
                current = current.sub_directories[target]

        if command.startswith("ls"):
            for header, name in map(str.split, command.splitlines()[1:]):
                if header == "dir":
                    current.sub_directories[name] = Directory(current)
                    all_directories.add(current.sub_directories[name])
                else:
                    current.file_size += int(header)

    print(f"Part 1: {sum(d.size for d in all_directories if d.size < 100_000)}")

    available = 70_000_000 - root.size
    required = 30_000_000 - available
    candidates = [d.size for d in all_directories if d.size > required]
    print(f"Part 2: {min(candidates)}\n")


solve(sample_input)
solve(actual_input)
