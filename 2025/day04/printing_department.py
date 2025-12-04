import aoc
import numpy as np
from numpy.typing import NDArray


def remove_rolls(grid: NDArray, recurse: bool = False) -> int:
    adjacent = aoc.np.count_adjacent(grid)
    removable = grid & (adjacent < 4)
    count = removable.sum()
    if not recurse or count == 0:
        return count
    return count + remove_rolls(grid & ~removable, recurse)


@aoc.register(__file__)
def answers():
    grid = np.where(np.asarray(aoc.read_grid()) == '@', 1, 0)
    yield remove_rolls(grid)
    yield remove_rolls(grid, recurse=True)

if __name__ == '__main__':
    aoc.run()
