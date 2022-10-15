import numpy as np


TREE = '#'
with open('2020/day3.txt') as f:
    TREE_MAP = np.array([list(line) for line in f.read().splitlines()])
print(TREE_MAP)

height, width = TREE_MAP.shape
print(f'{width}x{height}\n')


# Method One - One at a time indexing
def method_one(right, down):
    trees = 0
    loc = (0,0)
    while loc[0] < height:
        if TREE_MAP[loc] == TREE:
            trees += 1

        loc = (loc[0] + down, (loc[1] + right) % width)
    return trees


# Method Two - Rolling
def method_two(right, down):
    trees = 0
    traveled = 0
    rolled_map = TREE_MAP
    while traveled < height:
        if rolled_map[0][0] == TREE:
            trees += 1

        rolled_map = np.roll(rolled_map, (-down, -right), axis=(0, 1))
        traveled += down
    return trees


# Method Three - Multi-indexing
def method_three(right, down):
    points = np.full((height, 2), (down, right)).T * range(height)
    points = points[:, points[0] < height]
    points[1] = points[1] % width
    points = TREE_MAP[points[0], points[1]]
    return np.count_nonzero(points == TREE)



import timeit
from functools import reduce

print('-------- METHOD ONE --------')
print(method_one(3, 1))
print(timeit.Timer(lambda: method_one(3, 1)).timeit(100))
print('-------- METHOD TWO --------')
print(method_two(3, 1))
print(timeit.Timer(lambda: method_two(3, 1)).timeit(100))
print('-------- METHOD THREE --------')
print(method_three(3, 1))
print(timeit.Timer(lambda: method_three(3, 1)).timeit(100))

print('-------- PART TWO --------')
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
results = [method_three(right, down) for right, down in slopes]
print(reduce(lambda x, y: x*y, results))
