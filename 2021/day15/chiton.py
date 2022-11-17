from __future__ import annotations
import aoc
from collections import defaultdict
from dataclasses import dataclass, field
import heapq
import numpy as np
from numpy.typing import NDArray
from queue import PriorityQueue
from typing import Tuple


def adjacent_points(shape: tuple[int,int], point: tuple[int,int]) -> set[tuple[int,int]]:
    dirs = ((1, 0), (-1, 0), (0, 1), (-1, 0))
    adj = [(point[0]+d[0], point[1]+d[1]) for d in dirs]
    return {p for p in adj if p[0] in range(shape[0]) and p[1] in range(shape[1])}

def manhattan_dist(point1: tuple[int,int], point2: tuple[int,int]) -> int:
    return abs(point2[0] - point1[0]) + abs(point2[1] - point2[1])

def astar(grid: NDArray) -> int:
    start = (0, 0)
    end = (grid.shape[0] - 1, grid.shape[1] - 1)
    true_values = defaultdict(lambda: np.Inf)
    true_values[start] = 0
    
    path_stack = []
    visited = set()
    heapq.heappush(path_stack, (0, start))

    while path_stack:
        _, point = heapq.heappop(path_stack)
        if point == end:
            return true_values[point]
        if point in visited:
            continue
        visited.add(point)

        adjacents = adjacent_points(grid.shape, point) - visited
        for adj in adjacents:
            true = true_values[point] + grid[adj[1]][adj[0]]
            if true <= true_values[adj]:
                true_values[adj] = true
                f = manhattan_dist(adj, end) + true
                heapq.heappush(path_stack, (f, adj))

def expand_grid(grid: NDArray, n: int) -> NDArray:
    vertical = np.vstack([grid + row for row in range(n)])
    full_grid = np.hstack([vertical + col for col in range(n)])
    return np.where(full_grid > 9, full_grid - 9, full_grid)
    asdf = full_grid % 9
    return np.where(full_grid == 0, 9, full_grid)
    

@aoc.register(__file__)
def answers():
    grid = np.array([list(map(int, x)) for x in aoc.read_lines()])
    yield astar(grid)

    print(grid[-1][-1])
    grid = expand_grid(grid, 5).astype(int)
    print(grid[-1][-1])
    yield astar(grid)

if __name__ == '__main__':
    aoc.run(profile=True)
