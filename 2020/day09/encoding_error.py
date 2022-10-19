import itertools
import numpy as np
from typing import List


PREAMBLE = 25
def is_valid(window, test_value) -> bool:
    options = [sum(combo) for combo in itertools.combinations(window, 2)]
    return test_value in options


def find_weakness(window, target_value) -> List[int]:
    _window = np.array(window)
    data = np.array([(idx, val, sum(_window[:idx+1])) for idx, val in enumerate(_window)])
    while data.any():
        if target_value in data[:,2]:
            last_row = data[np.where(data[:,2] == target_value)][0]
            return list(_window[data[0][0] : last_row[0]])
        _row, data = data[0], data[1:]
        data[:,2] = data[:,2] - _row[2]
    raise Exception('Oopsie! Couldnt find weakness')


with open('2020/day09/data.txt') as f:
    data = [int(line) for line in f.read().splitlines()]

idx = PREAMBLE
while (is_valid(data[idx-PREAMBLE:idx], data[idx])):
    idx += 1
print(f'PART ONE: {data[idx]}')

weakness = find_weakness(data[:idx], data[idx])
print(f'PART TWO: {min(weakness) + max(weakness)}')
