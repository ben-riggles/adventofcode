from __future__ import annotations
from typing import Callable, ClassVar
import aoc
from dataclasses import dataclass, field
from functools import lru_cache
from math import prod, lcm
import re


@lru_cache
def is_prime(x: int) -> bool:
    for i in range(2, x//2 + 1):
        if x % i == 0:
            return False
    return True

@lru_cache
def prime_factors(x: int) -> set[int]:
    pfs = {i for i in range(2, x//2+1) if is_prime(i) and x % i == 0}
    return pfs if pfs else {x}


class Item:
    def __init__(self, start: int = 0):
        self.divisors: set[int] = prime_factors(start)
        self.offset: int = 0

    def __repr__(self):
        return f'Item(div={self.divisors}, offset={self.offset})'

    def __add__(self, val: int) -> Item:
        new_item = self.copy()
        new_item.offset += val
        return new_item

    def __mul__(self, val: int) -> Item:
        new_item = self.copy()
        new_item.divisors.add(val)
        new_item.offset *= val
        return new_item

    def copy(self) -> Item:
        new_item = Item()
        new_item.divisors = self.divisors
        new_item.offset = self.offset

@dataclass
class Monkey:
    id: int
    test: int = field(repr=False)
    items: list[Item] = field(default_factory=list)
    num_inspects: int = field(init=False, default=0, repr=False)
    _worry: Callable[[int], int] = field(init=False, default_factory=lambda: None, repr=False)
    _throw_target: Callable[[bool], int] = field(init=False, default_factory=lambda: None, repr=False)
    _ALL_MONKEYS: ClassVar[dict[int, Monkey]] = {}

    @classmethod
    def all(cls) -> dict[int, Monkey]:
        return cls._ALL_MONKEYS

    def __post_init__(self):
        Monkey._ALL_MONKEYS[self.id] = self

    def take_turn(self, relief: int):
        self.num_inspects += len(self.items)
        items = [self._worry(x) // relief for x in self.items]
        [self.throw(x) for x in items]
        self.items = []

    def throw(self, item):
        target = self._throw_target(item % self.test == 0)
        Monkey.all()[target].items.append(item)

    @staticmethod
    def parse_op_string(op_str: str) -> Callable[[int], int]:
        m = re.match(r'(.*) (\*|\+) (.*)', op_str).groups()
        op = prod if m[1] == '*' else sum
        return lambda x: op((x if m[0] == 'old' else int(m[0]), x if m[2] == 'old' else int(m[2])))

    @staticmethod
    def from_string(monkey_data: str) -> Monkey:
        regex =  r'Monkey (\d+):\n'
        regex += r'  Starting items: (.*)\n'
        regex += r'  Operation: new = (.*)\n'
        regex += r'  Test: divisible by (\d+)\n'
        regex += r'    If true: throw to monkey (\d+)\n'
        regex += r'    If false: throw to monkey (\d+)'
        m = re.match(regex, monkey_data).groups()
        
        monkey_id, op_str, test_val = int(m[0]), m[2], int(m[3])
        true_throw, false_throw = int(m[4]), int(m[5])
        items = [Item(int(x.strip())) for x in m[1].split(',')]

        retval = Monkey(id=monkey_id, test=test_val, items=items)
        retval._worry = Monkey.parse_op_string(op_str)
        retval._throw_target = lambda x: true_throw if x else false_throw
        return retval

@aoc.register(__file__)
def answers():
    monkeys = [Monkey.from_string(x) for x in aoc.read_chunks('small')]
    print(Monkey.all())

    # for _ in range(2000):
    #     for monkey in monkeys:
    #         monkey.take_turn(relief=1)
    # monkey_business = sorted([x.num_inspects for x in monkeys])[-2:]
    # yield prod(monkey_business)

if __name__ == '__main__':
    aoc.run()
