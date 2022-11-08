import numpy as np
from numpy.typing import NDArray
from typing import Dict, List


with open('2020/day23/data.txt') as f:
    cups = [int(x) for x in f.read()]


def destination(current: int, moving: List[int], max_cup: int) -> int:
    while True:
        current = current -1 if current > 1 else max_cup
        if current not in moving:
            return current


def move(cups: Dict[int,int], current_cup: int, max_cup: int) -> int:
    next1 = cups[current_cup]
    next2 = cups[next1]
    next3 = cups[next2]
    next4 = cups[next3]
    moving_cups = [next1, next2, next3]
    dest = destination(current_cup, moving_cups, max_cup)

    cups[current_cup] = next4
    cups[next3] = cups[dest]
    cups[dest] = next1
    return next4


cup_dict = {}
try:
    for idx, cup in enumerate(cups):
        cup_dict[cup] = cups[idx+1]
except IndexError:
    cup_dict[cups[-1]] = cups[0]

current_cup = cups[0]
for turn in range(100):
    current_cup = move(cup_dict, current_cup, 9)

cup_list = [cup_dict[1]]
while cup_list[-1] != 1:
    cup_list.append(cup_dict[cup_list[-1]])
cup_list = ''.join([str(x) for x in cup_list[:-1]])
print(f'PART ONE: {cup_list}')


cup_dict = {}
try:
    for idx, cup in enumerate(cups):
        cup_dict[cup] = cups[idx+1]
except IndexError:
    cup_dict[cups[-1]] = 10

for i in range(10, 1000000):
    cup_dict[i] = i+1
cup_dict[1000000] = cups[0]

current_cup = cups[0]
for turn in range(10000000):
    current_cup = move(cup_dict, current_cup, 1000000)

next1 = cup_dict[1]
next2 = cup_dict[next1]
print(f'PART TWO: {next1*next2}')
