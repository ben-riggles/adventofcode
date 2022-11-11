import aoc
import itertools
import numpy as np
from numpy.typing import NDArray


ACTIVE, INACTIVE = '#', '.'
NUM_CYCLES = 6

def create_grid(dimensions: int, init: NDArray, border: int = NUM_CYCLES) -> NDArray:
    init_size = max(init.shape)
    grid_size = init_size + 2 * border
    grid = np.full([grid_size] * dimensions, INACTIVE)

    _slice = slice(border, border + init_size)
    start_slice = (grid_size//2,)*(dimensions-2) + (_slice, _slice)
    grid[start_slice] = init
    return grid

def active_neighbors(grid: NDArray) -> NDArray:
    return sum([
        np.roll(grid, tuple(x), axis=tuple(range(grid.ndim))) == ACTIVE 
        for x in itertools.product((-1, 0, 1), repeat=grid.ndim)
        if x != (0,) * grid.ndim
    ])

def run_cycle(grid: NDArray) -> NDArray:
    neighbors = active_neighbors(grid)
    rule_one = np.logical_and(grid == ACTIVE, np.logical_or(neighbors < 2, neighbors > 3))
    rule_two = np.logical_and(grid == INACTIVE, neighbors == 3)

    retval = np.copy(grid)
    retval[rule_one] = INACTIVE
    retval[rule_two] = ACTIVE
    return retval


def main():
    aoc.setup(__file__)
    initial_state = np.array(list(map(list, aoc.read_lines())))

    grid1 = create_grid(dimensions=3, init=initial_state)
    for _ in range(NUM_CYCLES):
        grid1 = run_cycle(grid1)
    aoc.answer(1, np.count_nonzero(grid1 == ACTIVE))

    grid2 = create_grid(dimensions=4, init=initial_state)
    for _ in range(NUM_CYCLES):
        grid2 = run_cycle(grid2)
    aoc.answer(2, np.count_nonzero(grid2 == ACTIVE))

if __name__ == '__main__':
    main()
