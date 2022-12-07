"""https://adventofcode.com/2022/day/7"""

from __future__ import annotations
import os

from dataclasses import dataclass, field

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


@dataclass
class File:
    size: int
    name: str


@dataclass
class Directory:
    name: str
    parent_dir: Directory | None = None
    files: dict[str, File] = field(default_factory=dict)
    directories: dict[str, Directory] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return sum(x.size for x in self.files.values()) + sum(
            x.size for x in self.directories.values()
        )

    @property
    def path(self) -> str:
        if self.parent_dir is None:
            return ""
        return f"{self.parent_dir.path}/{self.name}"


def solve(inputs: str) -> None:
    commands = inputs.split("$ ")

    root_dir = Directory("/")
    current_dir = root_dir
    all_directories = {"/": root_dir}

    for command in commands:
        if not command:
            continue
        lines = command.splitlines()
        instruction, output = lines[0], lines[1:]

        if instruction.startswith("cd"):
            _, target = instruction.split()
            if target == "/":
                current_dir = root_dir
            elif target == "..":
                assert current_dir.parent_dir is not None
                current_dir = current_dir.parent_dir
            else:
                current_dir = current_dir.directories[target]

        if instruction.startswith("ls"):
            for item in output:
                token_1, name = item.split()
                if token_1 == "dir":
                    if name not in current_dir.directories:
                        new_dir = Directory(name, current_dir)
                        current_dir.directories[name] = new_dir
                        all_directories[new_dir.path] = new_dir
                else:
                    if name not in current_dir.files:
                        current_dir.files[name] = File(size=int(token_1), name=name)

    print(
        f"Part 1: {sum(d.size for d in all_directories.values() if d.size < 100_000)}"
    )

    current_dir = root_dir
    available = 70_000_000 - root_dir.size
    required = 30_000_000 - available

    candidates = [d.size for d in all_directories.values() if d.size > required]

    print(f"Part 2: {min(candidates)}\n")


solve(sample_input)
solve(actual_input)
