from __future__ import annotations

import os

from functools import reduce
from itertools import product

from utils import  print_time_taken

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
    def __init__(self, input_string, parent=None) -> None:
        self.parent = parent
        self.depth = self.parent.depth+1 if self.parent else 0
        self.left= None
        self.right = None
        self.value = None
        
        if input_string.isdigit():
            self.depth = None
            self.value = int(input_string)
            return

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
        left, right =  input_string[1:comma_position], input_string[comma_position+1:-1]
        self.left =  SnailfishNumber(left, self)
        self.right =  SnailfishNumber(right, self)
        
    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'if self.value is None else str(self.value) 

    def __add__(self, other):
        return SnailfishNumber(f'[{self},{other}]').reduce()
    
    @property
    def magnitude(self)-> int:
        _magnitude = lambda x: x.magnitude if x.value is None else x.value
        return 3 * _magnitude(self.left) + 2 * _magnitude(self.right)
    
    @classmethod
    def ordered_values(cls,n: SnailfishNumber):
        if n.value is not None:
            return [n]
        return cls.ordered_values(n.left) +cls.ordered_values(n.right)

    def value_above_nine(self):
        integers_above_nine = [n for n in self.ordered_values(self) if n.value > 9]
        return integers_above_nine[0] if integers_above_nine else None

    def pair_at_depth_four(self):
        if self.depth == 4 and self.left and self.right:
            return self
        for child in (self.left, self.right):
            if child and child.pair_at_depth_four():
                return child.pair_at_depth_four()
        return None

    def reduce(self):
        while self.pair_at_depth_four() or self.value_above_nine():
            
            while to_explode := self.pair_at_depth_four():
                ordered_values = self.ordered_values(self)
                for node_index, node in enumerate(ordered_values):
                    if node.parent == to_explode:
                        break
                for delta, explode in zip((-1,+2), (to_explode.left, to_explode.right)):
                    if 0 <=node_index+delta <len(ordered_values):
                        ordered_values[node_index+delta].value += explode.value
                to_explode.value = 0
                to_explode.left, to_explode.right = None, None

            if node:=self.value_above_nine():
                node.depth = node.parent.depth + 1
                node.left = SnailfishNumber(f'{node.value//2}', node)
                node.right = SnailfishNumber(f'{(node.value+1)//2}', node)
                node.value = None

        return self



REDUCTION_TESTS = {
    "[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
    "[7,[6,[5,[4,[3,2]]]]]": "[7,[6,[5,[7,0]]]]",
    "[[6,[5,[4,[3,2]]]],1]": "[[6,[5,[7,0]]],3]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
    "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]": "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
    "[[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]": "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
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


for n, answer in RANGE_TESTS.items():
    test_numbers = [SnailfishNumber(f"[{i},{i}]") for i in range(1, n + 1)]
    assert str(reduce(lambda a, b: a + b, test_numbers)) == answer

for test, answer in REDUCTION_TESTS.items():
    assert str(SnailfishNumber(test).reduce()) == answer

test_numbers = [SnailfishNumber(line) for line in SUM_TEST.splitlines()]
sum_test = reduce(lambda a, b: a + b, test_numbers)
assert str(sum_test) == SUM_TEST_ANSWER
