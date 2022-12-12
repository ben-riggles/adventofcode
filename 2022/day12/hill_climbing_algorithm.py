import heapq
import aoc
import numpy as np
from numpy.typing import NDArray
import sys


Point = tuple[int, int]

def adjacent_points(shape: tuple[int,int], point: Point) -> set[Point]:
    adj = [
        (point[0] + 1, point[1]), (point[0] - 1, point[1]),
        (point[0], point[1] + 1), (point[0], point[1] - 1)
    ]
    return {p for p in adj if (0 <= p[0] < shape[0]) and (0 <= p[1] < shape[1])}

def manhattan_dist(point1: Point, point2: Point) -> int:
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

def astar(grid: NDArray, start: Point = None, _max: int = None) -> int:
    if start is None:
        start = np.where(grid == 0)
        start = (start[0][0], start[1][0])
    end = np.where(grid == 27)
    end = (end[0][0], end[1][0])

    path_stack = []
    visited = set()
    heapq.heappush(path_stack, (0, 0, start))

    while path_stack:
        _, true_value, point = heapq.heappop(path_stack)
        if point == end:
            return true_value
        if point in visited:
            continue
        if _max is not None and true_value > _max:
            return sys.maxsize
        visited.add(point)

        point_val = grid[point[0]][point[1]]

        asdf = adjacent_points(grid.shape, point)
        adjacents = asdf - visited
        for adj in adjacents:
            adj_val = grid[adj[0]][adj[1]]
            man_dist = manhattan_dist(end, adj)
            if adj_val - point_val > 1:
                continue
            modifier = -1 * (adj_val - point_val)
            heapq.heappush(path_stack, (man_dist + modifier + true_value, true_value + 1, adj))
    return sys.maxsize


def convert_letter(char: str) -> int:
    match char:
        case 'S': return 0
        case 'E': return 27
        case _: return ord(char) - ord('a') + 1


@aoc.register(__file__)
def answers():
    height_map = np.vectorize(convert_letter)(aoc.read_grid())
    yield astar(height_map)

    height_map[height_map == 0] = 1
    possible_starts = np.where(height_map == 1)

    best_trail = sys.maxsize
    for start in zip(*possible_starts):
        best_trail = min(best_trail, astar(height_map, start=start, _max=best_trail))
    yield best_trail

if __name__ == '__main__':
    aoc.run()
