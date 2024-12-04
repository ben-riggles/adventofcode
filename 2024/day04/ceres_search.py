import aoc
import itertools
import numpy as np
from numpy.typing import NDArray


def count_xmas(arr: NDArray) -> int:
    arr_as_str = ''.join(arr)
    return arr_as_str.count('XMAS') + arr_as_str.count('SAMX')

def is_x_mas(arr: NDArray, x: int, y: int) -> bool:
    try:
        diag_one = arr[y-1][x-1], arr[y+1][x+1]
        diag_two = arr[y-1][x+1], arr[y+1][x-1]
    except IndexError:
        return False
    return 'M' in diag_one and 'S' in diag_one and 'M' in diag_two and 'S' in diag_two

@aoc.register(__file__)
def answers():
    word_search = np.array(aoc.read_grid())

    # Part One
    n_rows, n_cols = word_search.shape
    rows = (x for x in word_search)
    cols = (x for x in word_search.T)
    f_diags = (np.diag(word_search, k=x) for x in range(-n_cols, n_rows))
    b_diags = (np.diag(np.fliplr(word_search), k=x) for x in range(-n_cols, n_rows))
    yield sum(count_xmas(x) for x in itertools.chain(rows, cols, f_diags, b_diags))

    # Part Two
    idxs = ((x, y) for y, x in zip(*np.where(word_search == 'A')))
    yield sum(is_x_mas(word_search, *idx) for idx in idxs)

if __name__ == '__main__':
    aoc.run()
