from __future__ import annotations
import collections
from typing import Set, Counter


class BagTree:
    def __init__(self):
        self.bags = {}

    def __getitem__(self, color: str) -> Bag:
        if color not in self.bags:
            self.bags[color] = Bag(color)
        return self.bags[color]


class Bag:
    def __init__(self, color: str):
        self.color: str = color
        self.parents: Counter[Bag] = collections.Counter({})
        self.children: Counter[Bag] = collections.Counter({})

    def __str__(self):
        return self.color

    def __repr__(self):
        return f'Bag({self.color})'

    def add_child(self, other: Bag, amount: int):
        self.children[other] = amount
        other.parents[self] = amount

    @staticmethod
    def from_string(data: str, tree: BagTree):
        color, children = data.split('bags contain')
        bag = tree[color.strip()]

        if 'no other bags' in children:
            return

        children = children.replace('.', '').replace('bags', '').replace('bag', '').split(',')
        for child in children:
            amount, child_color = child.strip().split(' ', maxsplit=1)
            bag.add_child(tree[child_color.strip()], int(amount.strip()))


tree = BagTree()
with open('2020/day07/data.txt') as f:
    [Bag.from_string(line, tree) for line in f.read().splitlines()]


def all_parents(bag: Bag) -> Set[Bag]:
    retval = set(bag.parents.keys())

    parents = [all_parents(x) for x in bag.parents.keys()]
    if parents:
        retval = retval.union(*parents)
    return retval

shiny_gold_parents = all_parents(tree['shiny gold'])
print(f'PART ONE: {len(shiny_gold_parents)}')


def all_children(bag: Bag, amount: int = 1) -> Counter[Bag]:
    retval = Counter({k: v*amount for k, v in bag.children.items()})
    retval = sum([all_children(key, value) for key, value in retval.items()], start=retval)
    return retval

shiny_gold_children = all_children(tree['shiny gold'])
print(f'PART TWO: {sum(shiny_gold_children.values())}')
