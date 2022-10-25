from __future__ import annotations
from abc import ABC, abstractmethod
import re
from typing import List


def evaluate(eq: str) -> int:
    eq = eq.replace('(', '( ').replace(')', ' )').split(' ')
    left = eq.pop(0)



    while ('(' in eq):
        paren = re.search(r'\((.*?)\)', eq).group(1)
        result = evaluate(paren)
        eq = eq.replace(f'({paren})', str(result))

    eq_list = eq.split(' ')
    retval = int(eq_list.pop(0))
    while eq_list:
        op = eq_list.pop(0)
        right = int(eq_list.pop(0))

        match op:
            case '+': retval += right
            case '*': retval *= right
            case _: raise
    return retval


with open('2020/day18/small.txt') as f:
    equations = f.read().splitlines()

results = [evaluate(eq) for eq in equations]