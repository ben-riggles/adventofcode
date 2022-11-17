import numpy as np
import sys
from dataclasses import dataclass, field
from typing import Tuple


# @dataclass
# class Location:
#     x: int
#     y: int

# @dataclass(order=True)
# class Path:
#     visited: set[Location] = field(default_factory=set, compare=False)
#     value: int = 0


# @dataclass(order=True)
# class Node:
#     point: Tuple[int, int] = field(compare=False)
#     value: int = field(compare=False)
#     distance: int = field(default=sys.maxsize)
#     visited: bool = field(default=False)


# with open('2021/day15/risk_level.txt') as f:
#     grid = f.read().splitlines()

# base_array = np.array([[int(val) for val in list(row)] for row in grid])
# print(base_array)

# vert_array = []
# for i in range(5):
#     new_array = base_array + i
#     new_array = np.where(new_array > 9, new_array - 9, new_array)
#     vert_array.append(new_array)
# vert_array = np.concatenate(vert_array)

# full_grid = []
# for i in range(5):
#     new_array = vert_array + i
#     new_array = np.where(new_array > 9, new_array - 9, new_array)
#     full_grid.append(new_array)
# full_grid = np.concatenate(full_grid, axis=1)

# risk_grid = []
# for y, row in enumerate(full_grid):
#     risk_grid.append([Node((x,y), int(val)) for x, val in enumerate(list(row))])
# risk_grid = np.array(risk_grid)
# end_node = risk_grid[(risk_grid.shape[0]-1, risk_grid.shape[1]-1)]
# print(end_node)


# def check_neighbor(node, point, queue):
#     if point[0] < risk_grid.shape[0] and point[1] < risk_grid.shape[1] and point[0] >= 0 and point[1] >= 0:
#         neighbor = risk_grid[point[1]][point[0]]
#     else:
#         return
#     if not neighbor.visited:
#         if neighbor.distance == sys.maxsize:
#             queue.append(neighbor)
#         neighbor.distance = min(node.distance + neighbor.value, neighbor.distance)


# start_node = risk_grid[0][0]
# start_node.distance = 0

# queue = [start_node]
# while(queue):
#     node = min(queue)
#     queue.remove(node)
#     node.visited = True
#     if node == end_node:
#         break

#     check_neighbor(node, (node.point[0], node.point[1]+1), queue)
#     check_neighbor(node, (node.point[0]+1, node.point[1]), queue)
#     check_neighbor(node, (node.point[0], node.point[1]-1), queue)
#     check_neighbor(node, (node.point[0]-1, node.point[1]), queue)

# print(end_node.distance)



from numpy import Inf
import heapq

def main():
    with open('2021/day15/data.txt') as f:
        data = [[int(i) for i in j] for j in f.read().splitlines()]

    max_l = len(data[0])
    data, max_l = extend_data(data)

    solution = astar_solve(data, max_l)
    print(solution)


def astar_solve(data, max_l):
    '''solve the puzzle with given input array using A* and a heap queue'''

    start_node = (0, 0)
    end_node = (max_l - 1, max_l - 1)

    open_queue = []
    closed_queue = set()
    parents = {}
    g_score = {}

    for y in range(len(data)):
        for x in range(len(data)):
            g_score[(y, x)] = Inf # Set g(n) to infinite for all nodes

    g_score[start_node] = 0 # Let g(n) for start node = 0
    heapq.heappush(open_queue, (get_cityblock(start_node, end_node), start_node)) # add start node to queue

    while open_queue:
        _, node = heapq.heappop(open_queue) # pop the node with lowest f(n)

        if node == end_node:
            # if we have reached the goal node, trace back path and add up total
            total = 0

            while node in parents:
                x = node[0]
                y = node[1]
                total += data[y][x]
                node = parents[node]
            return total

        elif node in closed_queue:
            continue # if node in closed queue, skip

        else:
            neighbours = get_neighbours(data, node)

            for neighbour in neighbours:
                if neighbour in closed_queue:
                    continue # if neighbour in closed queue, skip
                x = neighbour[0]
                y = neighbour[1]
                added_g_score = data[y][x]

                candidate_g = g_score[node] + added_g_score

                if candidate_g <= g_score[neighbour]:
                    g_score[neighbour] = candidate_g
                    parents[neighbour] = node
                    f = get_cityblock(neighbour, end_node) + candidate_g # calculate f(n) = h(n) + g(n)
                    heapq.heappush(open_queue, (f, neighbour)) # add neighbour and its f(n) to the heap

            closed_queue.add(node)


def get_cityblock(a, b):
    '''return cityblock distance from node a to node b'''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbours(data, node):
    '''get neighbours of target node and check if within bounds'''
    x = node[0]
    y = node[1]
    node_neighbours = []

    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    for i in neighbours:
        if (0 <= i[0] <= len(data) - 1) and (0 <= i[1] <= len(data) - 1):
            node_neighbours.append(i) # append to list only if within bounds
    return node_neighbours


def extend_data(data):
    '''returns the data as a 2d array extended 5 times in each direction'''
    d = len(data)
    max_list_size = len(data) * 5
    extended_data = [[0 for _ in range(max_list_size)] for _ in range(max_list_size)] # pad an empty array with zeros

    for y_index, y in enumerate(extended_data):
        for x_index, x in enumerate(y):
            n = data[y_index % d][x_index % d]
            extended_data[y_index][x_index] = (n + ((y_index // d) + (x_index // d)) - 1) % 9 + 1 # formula: i = (n - 1) % 9 + 1

    return extended_data, max_list_size


if __name__ == '__main__':
    main()