import aoc
from dataclasses import dataclass, field
import heapq
import numpy as np
from numpy.typing import NDArray


Point = tuple[int, int]

def adjacent_points(shape: tuple[int,int], point: Point) -> set[Point]:
    adj = [
        (point[0] + 1, point[1]), (point[0] - 1, point[1]),
        (point[0], point[1] + 1), (point[0], point[1] - 1)
    ]
    return {p for p in adj if (0 <= p[0] < shape[0]) and (0 <= p[1] < shape[1])}

def manhattan_dist(point1: Point, point2: Point) -> int:
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])


@dataclass(order=True, kw_only=True)
class Node:
    estimated: int = 0
    true_value: int = 0
    point: Point = field(compare=False)
    visited: set[Point] = field(compare=False, default_factory=set)

def astar(grid: NDArray, start: Point, end_value: int) -> int:
    start_node = Node(point=start)
    start_value = grid[start]
    end_points = list(zip(*np.where(grid == end_value)))
    increasing = start_value < end_value

    path_stack = []
    heapq.heappush(path_stack, start_node)

    while path_stack:
        node: Node = heapq.heappop(path_stack)
        if node.point in end_points:
            return node.true_value
        if node.point in node.visited:
            continue
        point_val = grid[node.point]
        node.visited.add(node.point)

        for adj in adjacent_points(grid.shape, node.point) - node.visited:
            adj_val = grid[adj]
            diff = (adj_val - point_val) * (1 if increasing else -1)
            if diff > 1:
                continue
            
            for end in end_points:
                man_dist = manhattan_dist(end, adj)
                modifier = -5 if diff == 1 else diff

                new_node = Node(
                    estimated = man_dist + modifier + node.true_value,
                    true_value = node.true_value + 1,
                    point = adj,
                    visited = node.visited
                )
                heapq.heappush(path_stack, new_node)


def convert_letter(char: str) -> int:
    match char:
        case 'S': return 0
        case 'E': return 27
        case _: return ord(char) - ord('a') + 1


@aoc.register(__file__)
def answers():
    height_map = np.vectorize(convert_letter)(aoc.read_grid())

    start = list(zip(*np.where(height_map == 0)))[0]
    yield astar(height_map, start=start, end_value=27)

    height_map[height_map == 0] = 1
    start = list(zip(*np.where(height_map == 27)))[0]
    yield astar(height_map, start=start, end_value=1)

if __name__ == '__main__':
    aoc.run()
