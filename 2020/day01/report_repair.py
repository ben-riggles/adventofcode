import itertools
import numpy as np


def find_combo(data, target, len):
    for combo in itertools.combinations(data, len):
        if sum(combo) == target:
            return np.prod(combo)


with open('2020/day01/data.txt') as f:
    data = [int(line) for line in f.read().splitlines()]
    
print(f'PART ONE: {find_combo(data, 2020, 2)}')
print(f'PART TWO: {find_combo(data, 2020, 3)}')
