import aoc
from collections import Counter
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve
import re


DIRECTIONS = {
    'w': (0, -1), 'nw': (-1, -1), 'ne': (-1, 0),
    'e': (0, 1), 'se': (1, 1), 'sw': (1, 0)
}

def initial_state(lines: list[str]) -> list[tuple]:
    delims = '|'.join(DIRECTIONS.keys())
    lines = [list(filter(None, re.split(f'({delims})', line))) for line in lines]
    coords = Counter([tuple(sum(np.array([DIRECTIONS[x] for x in line]))) for line in lines])
    return [coord for coord, count in coords.items() if count % 2 != 0]

def process_days(black_tiles: NDArray, num_days: int) -> NDArray:
    black_tiles = black_tiles.T
    init_shape = np.ptp(black_tiles, axis=1)
    init_shape = np.zeros(init_shape+1, dtype=int)
    min_value = np.min(black_tiles, axis=1, keepdims=True)
    init_shape[tuple(black_tiles - min_value)] = 1
    black_tiles = np.pad(init_shape, num_days)

    kernel = [
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1]
    ]
    for _ in range(num_days):
        neighbors = convolve(black_tiles, kernel, mode='constant')
        black_tiles = black_tiles & (neighbors == 1) | (neighbors == 2)
    return black_tiles


def main():
    aoc.setup(__file__)
    lines = aoc.read_lines()

    black_tiles = np.array(initial_state(lines))
    aoc.answer(1, len(black_tiles))

    black_tiles = process_days(black_tiles, num_days=100)
    aoc.answer(2, np.sum(black_tiles))


if __name__ == '__main__':
    main()
