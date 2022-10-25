import numpy as np

with open('2021/day11/energy_levels.txt') as f:
    energy_levels = f.read().splitlines()
energy_levels = np.array([np.array(list(str(x)), dtype=int) for x in energy_levels])
print(energy_levels)

# Part 1
print('---------- Part 1 ----------')

def adjacent_points(indices, shape):
    # Get all adjacent points
    left = indices[0] - 1
    right = indices[0] + 1
    up = indices[1] - 1
    down = indices[1] + 1
    adjacent = (
        np.concatenate([indices[0], right, right, right, indices[0], left, left, left]),
        np.concatenate([up, up, indices[1], down, down, down, indices[1], up])
    )

    # Remove points outside of the possible range
    adjacent = list(zip(adjacent[0], adjacent[1]))
    adjacent = [x for x in adjacent if x[0] >= 0 and x[0] < shape[0] and x[1] >= 0 and x[1] < shape[1]]
    return adjacent

def step(energy):
    energy += 1
    flash_count = 0
    while ((energy > 9).sum() > 0):
        flashes = np.where(energy > 9)
        energy[flashes] = -99
        flash_count += len(flashes[0])

        for x, y in adjacent_points(flashes, energy.shape):
            energy[x][y] += 1
    energy[energy < 0] = 0
    return flash_count


# Part 2
print('---------- Part 2 ----------')
i = 0
while(np.any(energy_levels)):
    step(energy_levels)
    i += 1
print(f'{i=}')
