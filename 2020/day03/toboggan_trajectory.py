import aoc
from math import prod
import numpy as np
from numpy.typing import NDArray


TREE = '#'

def count_trees(tree_map: NDArray, right: int, down: int) -> int:
    height, width = tree_map.shape
    points = np.full((height, 2), (down, right)).T * range(height)
    points = points[:, points[0] < height]
    points[1] = points[1] % width
    points = tree_map[points[0], points[1]]
    return np.count_nonzero(points == TREE)

def main():
    aoc.setup(__file__)
    tree_map = np.array(list(map(list, aoc.read_lines())))
    aoc.answer(1, count_trees(tree_map, 3, 1))

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    results = [count_trees(tree_map, right, down) for right, down in slopes]
    aoc.answer(2, prod(results))

if __name__ == '__main__':
    main()
