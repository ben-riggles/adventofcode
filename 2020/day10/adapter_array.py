import aoc
import itertools
import functools
import numpy as np
from numpy.typing import NDArray


def num_choices(ar: NDArray, jolts: int) -> int:
    diffs = ar - jolts
    return np.count_nonzero((diffs >= 1) & (diffs <= 3))

@functools.lru_cache()
def branches(chunk) -> int:
    if chunk == tuple(): return 1
    elif chunk == (2,): return 2
    return branches(chunk[1:]) + branches(chunk[2:]) + branches(chunk[3:])


def main():
    aoc.setup(__file__)
    adapters = np.array(list(map(int, aoc.read_lines())))
    adapters = np.sort(np.append(adapters, (0, max(adapters) + 3)))
    
    diff = adapters[1:] - np.roll(adapters, 1)[1:]
    ones, threes = np.count_nonzero(diff == 1), np.count_nonzero(diff == 3)
    aoc.answer(1, ones * threes)

    choices = np.array([num_choices(adapters, x) for x in adapters])
    chunks = [list(x[1]) for x in itertools.groupby(choices, lambda x: x > 1) if x[0]]
    branch_list = [branches(tuple(chunk)) for chunk in chunks]
    num_branches = functools.reduce(lambda x, y: x*y, branch_list)
    aoc.answer(2, num_branches)

if __name__ == '__main__':
    main()
