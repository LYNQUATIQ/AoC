"""https://adventofcode.com/2021/day/18"""
from __future__ import annotations

import os
import re
from functools import reduce
from itertools import product

with open(os.path.join(os.path.dirname(__file__), f"inputs/day18_input.txt")) as f:
    actual_input = f.read()


sample_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


class SnailfishNumber:
    
    def __init__(self, parent=None, left=None, right=None, value=None) -> None:
        self.parent = parent
        self.left, self.right = left, right
        self.value = value
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    @classmethod
    def create(cls, input_string, parent=None) -> None:
        snailfish_number = cls(parent)

        if input_string.isdigit():
            snailfish_number.value = int(input_string)
            return snailfish_number

        bracket_count = 0
        for comma_position, c in enumerate(input_string):
            match c:
                case '[':
                    bracket_count +=1
                case ']':
                    bracket_count -=1
                case ',':
                    if bracket_count==1:
                        break
        left, right = input_string[1:comma_position], input_string[comma_position+1:-1]
        snailfish_number.left = SnailfishNumber.create(left, snailfish_number)
        snailfish_number.right = SnailfishNumber.create(right, snailfish_number)
        return snailfish_number
        
    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]' if self.value is None else str(self.value)

    def __add__(self, other):
        return SnailfishNumber(left=self, right=other).reduce()

    @property
    def depth(self):
        return 0 if self.parent is None else self.parent.depth + 1

    @property
    def magnitude(self)-> int:
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude + 2 * self.right.magnitude
    
    def depth_four(self):
        if self.depth == 4:
            return self
        for child in (self.left, self.right):
            if child.value is not None:
                child_at_depth_four = child.depth_four()
                if child_at_depth_four:
                    return child_at_depth_four
        return None

    def ordered_ints(self, limit=-1):
        if self.value is not None:
            return [self] if self.value > limit else []
        return self.left.ordered_ints(limit) + self.right.ordered_ints(limit)
    
    def above_nine(self):
        retval = self.ordered_ints(9)
        return retval[0] if retval else None

    @staticmethod
    def split(v:int, parent: SnailfishNumber)->SnailfishNumber:
        return SnailfishNumber(f'[{v//2},{(v+1)//2}]', parent)
    
    def reduce(self):
        while self.depth_four() or self.above_nine():
            while pair_to_explode := self.depth_four():
                ordered_nodes = self.ordered_ints()
                for i, node in enumerate(ordered_nodes):
                    if node == pair_to_explode:
                        break

                left,right = ordered_nodes[:i], ordered_nodes[i+2:]
                if left:
                    left[-1].value += pair_to_explode.left
                if right:
                    right[0].value += pair_to_explode.right
                if pair_to_explode.parent.left == pair_to_explode:
                    pair_to_explode.parent.left = 0
                else:
                    pair_to_explode.parent.right = 0

            if pair_above_nine:=self.above_nine():
                if isinstance(pair_above_nine.left, int) and pair_above_nine.left > 9:
                    pair_above_nine.left = self.split(pair_above_nine.left, pair_above_nine)
                else:
                    pair_above_nine.right = self.split(pair_above_nine.right, pair_above_nine)
        return self



def solve(inputs):
    numbers = [SnailfishNumber.create(line) for line in inputs.splitlines()]
    
    print(f"Part 1: {reduce(lambda a,b:a+b, numbers).magnitude}")

    magnitude = 0
    for a, b in product(numbers, numbers):
        if a != b:
            magnitude=max((SnailfishNumber(a)+SnailfishNumber(b)).magnitude,magnitude)
    print(f"Part 2: {magnitude}\n")


solve(sample_input)
solve(actual_input)