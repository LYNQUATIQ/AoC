"""https://adventofcode.com/2021/day/18"""
from __future__ import annotations

import logging
import os
import re
from functools import reduce
from itertools import product

from utils import  print_time_taken

log_file = os.path.join(os.path.dirname(__file__), f"logs/day18.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w")
with open(os.path.join(os.path.dirname(__file__), f"inputs/day18_input.txt")) as f:
    actual_input = f.read()


REDUCTION_TESTS = {
    "[[[[[9,8],1],2],3],4]" : "[[[[0,9],2],3],4]",
    "[7,[6,[5,[4,[3,2]]]]]" : "[7,[6,[5,[7,0]]]]",
    "[[6,[5,[4,[3,2]]]],1]" : "[[6,[5,[7,0]]],3]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]" : "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
    "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]" : "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
    "[[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]":"[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]"
}

RANGE_TESTS = {
    4: "[[[[1,1],[2,2]],[3,3]],[4,4]]",
    5: "[[[[3,0],[5,3]],[4,4]],[5,5]]",
    6: "[[[[5,0],[7,4]],[5,5]],[6,6]]",
}

SUM_TEST = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""" 
SUM_TEST_ANSWER = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"


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
    def __init__(self, input_string, parent=None) -> None:
        self.parent = parent
        self.input_string = input_string

        try:
            left, right = re.match(r"^\[(\d),(\d)\]$", input_string).groups()
        except AttributeError:
            left, right = self._parse_input(input_string)

        self.left = int(left) if left.isdigit() else SnailfishNumber(left, self)
        self.right = int(right) if right.isdigit() else SnailfishNumber(right, self)
        
    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'

    def __add__(self, other):
        return SnailfishNumber(f'[{self},{other}]').reduce()
    
    @staticmethod
    def _parse_input(input_string):
        bracket_count = 0
        for i, c in enumerate(input_string):
            match c:
                case '[':
                    bracket_count +=1
                case ']':
                    bracket_count -=1
                case ',':
                    if bracket_count==1:
                        return (input_string[1:i],input_string[i+1:-1])
        raise ValueError

    @property
    def depth(self):
        return 0 if self.parent is None else self.parent.depth + 1

    @property
    def magnitude(self)-> int:
        left = self.left if isinstance(self.left, int) else self.left.magnitude
        right = self.right if isinstance(self.right, int) else self.right.magnitude
        return 3 * left + 2 * right
    
    def depth_four(self):
        if self.depth == 4:
            return self
        for child in (self.left, self.right):
            if not isinstance(child, int):
                child_at_depth_four = child.depth_four()
                if child_at_depth_four:
                    return child_at_depth_four
        return None

    def ordered_ints(self, limit=-1):
        left, right = None, None
        if isinstance(self.left, int):
            left = [(self,True)] if self.left > limit else []
        else:
            left = self.left.ordered_ints(limit)
        if isinstance(self.right, int):
            right = [(self,False)] if self.right > limit else []
        else:
            right = self.right.ordered_ints(limit)
        return left + right
    
    def above_nine(self):
        retval = self.ordered_ints(9)
        return retval[0][0] if retval else None

    @staticmethod
    def split(v:int, parent: SnailfishNumber)->SnailfishNumber:
        return SnailfishNumber(f'[{v//2},{(v+1)//2}]', parent)
    
    def reduce(self):
        while self.depth_four() or self.above_nine():
            while pair_to_explode := self.depth_four():
                # logging.info(f'Exploding: {pair_to_explode}')
                ordered_nodes = self.ordered_ints()
                for i, (node, _) in enumerate(ordered_nodes):
                    if node == pair_to_explode:
                        break
                left,right = ordered_nodes[:i], ordered_nodes[i+2:]
                if left:
                    node, lhs = left[-1]
                    if lhs:
                        node.left += pair_to_explode.left
                    else:
                        node.right += pair_to_explode.left
                if right:
                    node, lhs = right[0]
                    if lhs:
                        node.left += pair_to_explode.right
                    else:
                        node.right += pair_to_explode.right
                if pair_to_explode.parent.left == pair_to_explode:
                    pair_to_explode.parent.left = 0
                else:
                    pair_to_explode.parent.right = 0
                # logging.info(f'After explosion: {self}')

            if pair_above_nine:=self.above_nine():
                # logging.info(f'Splitting: {pair_above_nine}')
                if isinstance(pair_above_nine.left, int) and pair_above_nine.left > 9:
                    pair_above_nine.left = self.split(pair_above_nine.left, pair_above_nine)
                else:
                    pair_above_nine.right = self.split(pair_above_nine.right, pair_above_nine)
                # logging.info(f'After split: {self}')
        return self


for n, answer in RANGE_TESTS.items():
    test_numbers = [SnailfishNumber(f'[{i},{i}]') for i in range(1, n+1)]
    assert str(reduce(lambda a,b:a+b, test_numbers))== answer

for test, answer in REDUCTION_TESTS.items():
    assert str(SnailfishNumber(test).reduce()) == answer
    
test_numbers = [SnailfishNumber(line) for line in SUM_TEST.splitlines()]
assert str(reduce(lambda a,b:a+b, test_numbers)) == SUM_TEST_ANSWER


@print_time_taken
def solve(inputs):
    numbers = [SnailfishNumber(line) for line in inputs.splitlines()]
    
    final_sum = reduce(lambda a,b:a+b, numbers)
    print(f"Part 1: {final_sum.magnitude}")

    max_magnitude = 0
    for a, b in product(inputs.splitlines(), inputs.splitlines()):
        if a != b:
            max_magnitude=max((SnailfishNumber(a)+SnailfishNumber(b)).magnitude,max_magnitude )
    print(f"Part 2: {max_magnitude}\n")


solve(sample_input)
# solve(actual_input)