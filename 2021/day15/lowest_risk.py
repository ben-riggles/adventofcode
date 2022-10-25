import numpy as np
import sys
from dataclasses import dataclass, field
from typing import Tuple


@dataclass(order=True)
class Node:
    point: Tuple[int, int] = field(compare=False)
    value: int = field(compare=False)
    distance: int = field(default=sys.maxsize)
    visited: bool = field(default=False)


with open('day15/risk_level.txt') as f:
    grid = f.read().splitlines()

base_array = np.array([[int(val) for val in list(row)] for row in grid])
print(base_array)

vert_array = []
for i in range(5):
    new_array = base_array + i
    new_array = np.where(new_array > 9, new_array - 9, new_array)
    vert_array.append(new_array)
vert_array = np.concatenate(vert_array)

full_grid = []
for i in range(5):
    new_array = vert_array + i
    new_array = np.where(new_array > 9, new_array - 9, new_array)
    full_grid.append(new_array)
full_grid = np.concatenate(full_grid, axis=1)

risk_grid = []
for y, row in enumerate(full_grid):
    risk_grid.append([Node((x,y), int(val)) for x, val in enumerate(list(row))])
risk_grid = np.array(risk_grid)
end_node = risk_grid[(risk_grid.shape[0]-1, risk_grid.shape[1]-1)]
print(end_node)


def check_neighbor(node, point, queue):
    if point[0] < risk_grid.shape[0] and point[1] < risk_grid.shape[1] and point[0] >= 0 and point[1] >= 0:
        neighbor = risk_grid[point[1]][point[0]]
    else:
        return
    if not neighbor.visited:
        if neighbor.distance == sys.maxsize:
            queue.append(neighbor)
        neighbor.distance = min(node.distance + neighbor.value, neighbor.distance)


start_node = risk_grid[0][0]
start_node.distance = 0

queue = [start_node]
while(queue):
    node = min(queue)
    queue.remove(node)
    node.visited = True
    if node == end_node:
        break

    check_neighbor(node, (node.point[0], node.point[1]+1), queue)
    check_neighbor(node, (node.point[0]+1, node.point[1]), queue)
    check_neighbor(node, (node.point[0], node.point[1]-1), queue)
    check_neighbor(node, (node.point[0]-1, node.point[1]), queue)

print(end_node.distance)
