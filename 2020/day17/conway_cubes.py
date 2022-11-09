import aoc
import itertools
import numpy as np
from numpy.typing import NDArray


ACTIVE, INACTIVE = '#', '.'
NUM_CYCLES = 6

def create_grid(dimensions: int, init: NDArray, border: int = NUM_CYCLES) -> NDArray:
    init_hgt, init_wdt = init.shape
    grid_size = max(init_hgt, init_wdt) + 2 * border
    grid = np.full((grid_size,)*dimensions, INACTIVE)

    slice_x = slice(border, border + init_wdt)
    slice_y = slice(border, border + init_hgt)
    start_slice = (grid_size//2,)*(dimensions-2) + (slice_y, slice_x)
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
    initial_state = np.array(list(map(list, aoc.read_lines())))

    grid1 = create_grid(dimensions=3, init=initial_state)
    for _ in range(NUM_CYCLES):
        grid1 = run_cycle(grid1)
    part1 = np.count_nonzero(grid1 == ACTIVE)

    grid2 = create_grid(dimensions=4, init=initial_state)
    for _ in range(NUM_CYCLES):
        grid2 = run_cycle(grid2)
    part2 = np.count_nonzero(grid2 == ACTIVE)

    aoc.print_results(part1, part2)

if __name__ == '__main__':
    main()
