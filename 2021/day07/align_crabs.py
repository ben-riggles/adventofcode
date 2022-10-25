import numpy as np

with open('2021/day07/crab_positions.txt') as f:
    crabs = f.readlines()[0].strip().split(',')
crabs = np.asarray(list(map(int, crabs)), dtype=int)

# For part 1
fuel = [np.abs(crabs-x).sum() for x in range(0, np.max(crabs)+1)]

best_position = np.argmin(fuel)
print(best_position)
print(fuel[best_position])


print('-----------------------------')


def fuel_cost(dist):
    dist = np.where(dist > 0, dist+1, dist)
    return (dist * (dist-1)) / 2

# For part 2
fuel = [fuel_cost(crabs-x).sum() for x in range(0, np.max(crabs)+1)]
best_position = np.argmin(fuel)
print(best_position)
print(fuel[best_position])
