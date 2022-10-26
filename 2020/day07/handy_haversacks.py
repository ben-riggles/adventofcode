from __future__ import annotations
import collections
from typing import Set, Counter


class BagDict:
    def __init__(self):
        self.bags = {}

    def __getitem__(self, color: str) -> Bag:
        if color not in self.bags:
            self.bags[color] = Bag(color)
        return self.bags[color]


class Bag:
    def __init__(self, color: str):
        self.color: str = color
        self.parents: Set[Bag] = set()
        self.children: Counter[Bag] = collections.Counter({})

    def __repr__(self):
        return f'Bag({self.color})'

    def __eq__(self, other: Bag):
        return self.color == other.color

    def __hash__(self):
        return hash(self.color)

    def add_child(self, child: Bag, amount: int):
        self.children[child] = amount
        child.parents.add(self)

    def all_parents(self) -> Set[Bag]:
        ancestors = [x.all_parents() for x in self.parents]
        return self.parents.union(*ancestors)

    def all_children(self, amount: int = 1) -> Counter[Bag]:
        children = Counter({bag: num*amount for bag, num in self.children.items()})
        children = sum([child.all_children(num) for child, num in children.items()], start=children)
        return children

    @staticmethod
    def from_string(data: str, tree: BagDict):
        color, children = (x.strip() for x in data.split('bags contain'))
        bag = tree[color]

        if 'no other bags' in children:
            return

        children = [x.strip() for x in children.replace('.', '').replace('bags', '').replace('bag', '').split(',')]
        for child in children:
            amount, child_color = child.split(' ', maxsplit=1)
            bag.add_child(tree[child_color], int(amount))


bags = BagDict()
with open('2020/day07/data.txt') as f:
    [Bag.from_string(line, bags) for line in f.read().splitlines()]

shiny_gold_parents = bags['shiny gold'].all_parents()
print(f'PART ONE: {len(shiny_gold_parents)}')

shiny_gold_children = bags['shiny gold'].all_children()
print(f'PART TWO: {sum(shiny_gold_children.values())}')
