import numpy as np

with open('day06/lanternfish.txt') as f:
    ages = f.readlines()[0].strip().split(',')
ages = np.asarray(list(map(int, ages)), dtype=int)

ages = {
    0: len(ages[np.where(ages == 0)]),
    1: len(ages[np.where(ages == 1)]),
    2: len(ages[np.where(ages == 2)]),
    3: len(ages[np.where(ages == 3)]),
    4: len(ages[np.where(ages == 4)]),
    5: len(ages[np.where(ages == 5)]),
    6: len(ages[np.where(ages == 6)]),
    7: 0,
    8: 0
}

NUM_DAYS = 256
for day in range(0, NUM_DAYS):
    ages = {
        0: ages[1],
        1: ages[2],
        2: ages[3],
        3: ages[4],
        4: ages[5],
        5: ages[6],
        6: ages[7] + ages[0],
        7: ages[8],
        8: ages[0]
    }

total_fish = sum(ages.values())
print(total_fish)
