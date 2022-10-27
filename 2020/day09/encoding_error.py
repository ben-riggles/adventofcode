import itertools
import numpy as np
from numpy.typing import NDArray
from typing import Tuple


def is_valid(window: NDArray, test_value: int) -> bool:
    options = {sum(combo) for combo in itertools.combinations(window, 2)}
    return test_value in options


def find_weakness(window: NDArray, target_value: int) -> NDArray:
    def _weakness_range(sums: NDArray, target_value: int, start: int = 0) -> Tuple[int, int]:
        try:
            idx = np.where(sums == target_value)[0][0]
            return start, start + idx + 1
        except IndexError:
            sums = sums - sums[0]
            return _weakness_range(sums[1:], target_value, start+1)

    sums = np.cumsum(window)
    start, end = _weakness_range(sums, target_value)
    return window[start:end]


PREAMBLE = 25
with open('2020/day09/data.txt') as f:
    data = np.array([int(line) for line in f.read().splitlines()])

idx = PREAMBLE
while (is_valid(data[idx-PREAMBLE:idx], data[idx])):
    idx += 1
print(f'PART ONE: {data[idx]}')

weakness = find_weakness(data[:idx], data[idx])
print(f'PART TWO: {min(weakness) + max(weakness)}')
