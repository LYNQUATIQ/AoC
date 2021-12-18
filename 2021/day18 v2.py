"""https://adventofcode.com/2021/day/18"""
from __future__ import annotations

from abc import ABC, abstractmethod
import os

from collections import defaultdict, deque
from functools import reduce
from itertools import pairwise, product

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


class Node(ABC):
    
    def __init__(self, parent:Node|None) -> None:
        self.parent = parent

    @classmethod
    def create(cls, input_string:str, parent:Node = None) -> None:
        if input_string.isdigit():
            return IntegerNode(value=int(input_string), parent=parent)
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
        node =  PairNode(
            left=cls.create(input_string=left),
            right=cls.create(input_string=right), 
            parent=parent
        )
        return node
    
    @abstractmethod
    def magnitude(self):
        """ Return the magnitude"""

class IntegerNode(Node):
    def __init__(self, value:int, parent: Node| None=None) -> None:
        self.value = value
        super().__init__(parent)

    def __repr__(self) -> str:
        return str(self.value)
    
    def magnitude(self):
        return self.value
    
class PairNode(Node):
    def __init__(self, left:Node, right:Node, parent:Node| None=None) -> None:
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
        super().__init__(parent)

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'
    

    def magnitude(self):
        return 3 * self.left.magnitudee + 2 * self.right.magnitude


class SnailfishNumber:
    
    @classmethod
    def create(cls, input_string:str) -> None:
        return cls(pair_node=Node.create(input_string))

    def __init__(self, pair_node: PairNode) -> None:
        self.root_node = pair_node
        
        self.depths = defaultdict(deque)
        self.value_nodes = deque()
        
        to_visit = deque([(self.root_node, 0)])
        while to_visit:
            node, depth = to_visit.popleft()
            self.depths[depth].append(node)
            if isinstance(node, PairNode):
                to_visit.append((node.left, depth+1))
                to_visit.append((node.right, depth+1))
            else:
                self.value_nodes.append(node)

        
    def __repr__(self) -> str:
        return str(self.root_node)

    def __add__(self, other):
        self.root_node = PairNode(self.root_node, other.root_node)
        for i in range(4,0,-1):
            self.depths[i+1] = self.depths[i]
        self.depths[0] = [self.root_node]
        for depth, nodes in other.depths.items():
            self.depths[depth+1].append(nodes) 
        self.value_nodes += other.value_nodes
        self.reduce()

    def value_above_nine_index(self):
        for i, node in enumerate(self.value_nodes):
            if node.value > 9:
                return i
        return None
                    
    def reduce(self):
        while self.pair_at_depths[4] or self.value_above_nine() is not None:
            
            while to_explode := self.pair_at_depths[4].popleft():
                for node_index, node in enumerate(self.value_nodes):
                    if to_explode.left == node:
                        break
                left = self.value_nodes[:max(node_index-1,0)]
                right = self.value_nodes[min(node_index+2, len(self.value_nodes)):]
                if left:
                    left[-1].value += self.value_nodes[node_index]
                if right:
                    right[0].value += self.value_nodes[node_index+1]
                replacement = IntegerNode(0, to_explode.parent)
                if to_explode.parent.left == to_explode:
                    to_explode.parent.left = replacement
                else:
                    to_explode.parent.right = replacement
                self.value_nodes = left + [replacement] + right

            if node_index:=self.value_above_nine() is not None:
                node = self.value_nodes[node_index]
                replacement = PairNode(
                    left=IntegerNode(node.value//2),
                    right=IntegerNode((node.value+1)//2),
                    parent=node.parent,
                )
                self.value_nodes = left + [replacement.left, replacement.right] + right

                node.depth = node.parent.depth + 1
                node.left = SnailfishNumber(f'{node.value//2}', node)
                node.right = SnailfishNumber(f'{(node.value+1)//2}', node)
                node.value = None
                ordered_values = self.ordered_values(self)

        return self
    
    @property
    def magnitude(self)-> int:
        return self.root_node.magnitude
    




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
solve(actual_input)