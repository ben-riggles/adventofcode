import numpy as np

with open('day09/small.txt') as f:
    height_map = f.read().splitlines()

height_map = np.array([list(x) for x in height_map], dtype=int)
print(height_map)

# Part 1
print('---------- Part 1 ----------')

# Check right neighbor
right_mask = height_map[:, :-1] < height_map[:, 1:]
col = np.full((len(height_map), 1), True)
right_mask = np.hstack((right_mask, col))

# Check left neighbor
left_mask = height_map[:, 1:] < height_map[:, :-1]
left_mask = np.hstack((col, left_mask))

# Check lower neighbor
height_map_t = height_map.T
down_mask = height_map_t[:, :-1] < height_map_t[:, 1:]
row = np.full((len(height_map_t), 1), True)
down_mask = np.hstack((down_mask, row)).T

# Check upper neighbor
up_mask = height_map_t[:, 1:] < height_map_t[:, :-1]
up_mask = np.hstack((row, up_mask)).T

low_mask = left_mask & right_mask & down_mask & up_mask
print(low_mask)
low_points = np.where(low_mask == True)
risk_level = sum(height_map[low_points] + 1)
print(risk_level)


# Part 2
print('---------- Part 2 ----------')
def find_basin(point, indices=None):
    try:
        if height_map[point] == 9 or point[0] < 0 or point[1] < 0:
            return []
    except IndexError:
        return []

    original = False
    if indices is None:
        original = True
        indices = []
    if point in indices:
        return []

    new_points = [point]
    new_points.extend(find_basin((point[0]+1, point[1]), indices + new_points))
    new_points.extend(find_basin((point[0]-1, point[1]), indices + new_points))
    new_points.extend(find_basin((point[0], point[1]+1), indices + new_points))
    new_points.extend(find_basin((point[0], point[1]-1), indices + new_points))

    if original:
        return np.array(list(zip(*new_points)))
    else:
        return new_points

basins = [find_basin(x) for x in zip(low_points[0], low_points[1])]
sizes = [len(x[0]) for x in basins]
result = sorted(sizes)[-3:]
print(result[0] * result[1] * result[2])
