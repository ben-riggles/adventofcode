import itertools
import numpy as np


ACTIVE, INACTIVE = '#', '.'
NUM_CYCLES = 6

def create_grid(dimensions: int, init):
    init_hgt, init_wdt = init.shape
    border_size = NUM_CYCLES + 1
    grid_size = max(init_hgt, init_wdt) + 2*border_size
    grid = np.full((grid_size,)*dimensions, INACTIVE)

    slice_x = slice(border_size, border_size + init_wdt)
    slice_y = slice(border_size, border_size + init_hgt)
    start_slice = (grid_size//2,)*(dimensions-2) + (slice_y, slice_x)
    grid[start_slice] = initial_state
    return grid

def active_neighbors(grid) -> int:
    return sum([
        np.roll(grid, tuple(x), axis=tuple(range(grid.ndim))) == ACTIVE 
        for x in itertools.product((-1, 0, 1), repeat=grid.ndim)
        if x != (0,) * grid.ndim
    ])

def run_cycle(grid):
    neighbors = active_neighbors(grid)
    rule_one = np.logical_and(grid == ACTIVE, np.logical_or(neighbors < 2, neighbors > 3))
    rule_two = np.logical_and(grid == INACTIVE, neighbors == 3)

    retval = np.copy(grid)
    retval[rule_one] = INACTIVE
    retval[rule_two] = ACTIVE
    return retval


with open('2020/day17/data.txt') as f:
    initial_state = np.array([list(line) for line in f.read().splitlines()])

grid1 = create_grid(dimensions=3, init=initial_state)
for _ in range(NUM_CYCLES):
    grid1 = run_cycle(grid1)

active_cubes = np.count_nonzero(grid1 == ACTIVE)
print(f'PART ONE: {active_cubes}')


grid2 = create_grid(dimensions=4, init=initial_state)
for _ in range(NUM_CYCLES):
    grid2 = run_cycle(grid2)

active_cubes = np.count_nonzero(grid2 == ACTIVE)
print(f'PART TWO: {active_cubes}')
