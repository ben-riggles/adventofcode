import itertools
import functools
import numpy as np


with open('2020/day10/data.txt') as f:
    adapters = np.array([int(line) for line in f.read().splitlines()])

x = np.append(adapters, (0, max(adapters) + 3))

adapters = np.sort(np.append(adapters, (0, max(adapters) + 3)))
shifted = np.roll(adapters, 1)
diff = adapters[1:] - shifted[1:]  # type: ignore

ones, threes = np.count_nonzero(diff == 1), np.count_nonzero(diff == 3)
print(f'PART ONE: {ones * threes}')


def num_choices(ar, jolts) -> int:
    diffs = ar - jolts
    return np.count_nonzero((diffs >= 1) & (diffs <= 3))

@functools.lru_cache()
def branches(chunk) -> int:
    if chunk == tuple(): return 1
    elif chunk == (2,): return 2
    elif chunk == (3, 2): return 4
    return branches(chunk[1:]) + branches(chunk[2:]) + branches(chunk[3:])

choices = np.array([num_choices(adapters, x) for x in adapters])
choices[choices == 1] = 0

chunks = [list(x[1]) for x in itertools.groupby(choices, lambda x: x == 0) if not x[0]]
branch_list = [branches(tuple(chunk)) for chunk in chunks]
num_branches = functools.reduce(lambda x, y: x*y, branch_list)
print(f'PART TWO: {num_branches}')