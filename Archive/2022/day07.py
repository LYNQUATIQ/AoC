"""https://adventofcode.com/2022/day/7"""
from __future__ import annotations

import os

from abc import ABC, abstractmethod
from typing import cast

with open(os.path.join(os.path.dirname(__file__), "inputs/day07_input.txt")) as f:
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


class FileSystemObject(ABC):
    def __init__(self, container: Directory | None, name: str) -> None:
        self.container = container
        self.name = name

    @property
    @abstractmethod
    def size(self) -> int:
        """Returns the size of the file system object"""


class Directory(FileSystemObject):
    def __init__(self, container: Directory | None, name: str) -> None:
        super().__init__(container, name)
        self.contents: dict[str, FileSystemObject] = {}

    @property
    def size(self) -> int:
        return sum(x.size for x in self.contents.values())


class File(FileSystemObject):
    def __init__(self, container: Directory, name: str, size: int) -> None:
        super().__init__(container, name)
        self._size = size

    @property
    def size(self) -> int:
        return self._size


def solve(inputs: str) -> None:
    root = Directory(container=None, name="/")
    current = root
    all_directories = {root}

    for command in inputs.split("$ "):
        if command.startswith("cd"):
            _, target = command.split()
            if target == "/":
                current = root
            elif target == "..":
                assert current.container is not None
                current = current.container
            else:
                assert isinstance(current.contents[target], Directory)
                current = cast(Directory, current.contents[target])

        if command.startswith("ls"):
            for header, name in map(str.split, command.splitlines()[1:]):
                if header == "dir":
                    directory = Directory(current, name)
                    current.contents[name] = directory
                    all_directories.add(directory)
                else:
                    current.contents[name] = File(current, name, int(header))

    print(f"Part 1: {sum(d.size for d in all_directories if d.size < 100_000)}")

    available = 70_000_000 - root.size
    required = 30_000_000 - available
    candidates = [d.size for d in all_directories if d.size > required]
    print(f"Part 2: {min(candidates)}\n")


solve(sample_input)
solve(actual_input)
