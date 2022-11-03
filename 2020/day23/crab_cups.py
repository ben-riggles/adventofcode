import numpy as np
from numpy.typing import NDArray


with open('2020/day23/small.txt') as f:
    cups = np.array([int(x) for x in f.read()])
    
def move(cups: NDArray, max_val: int) -> NDArray:
    current_cup = cups[0]
    moving_cups = cups[1:4]
    cups = np.delete(cups, slice(1,4))
    dest_idx = np.argmax((cups - current_cup) % max_val) + 1
    cups = np.concatenate([cups[:dest_idx], moving_cups, cups[dest_idx:]])
    return np.roll(cups, -1)


cups1 = cups.copy()
for turn in range(100):
    cups1 = move(cups1, 9)
cups1 = np.roll(cups1, -1 * np.where(cups1 == 1)[0])
print(f'PART ONE: {"".join(str(x) for x in cups1[1:])}')


cups2 = np.concatenate((cups, np.arange(start=10, stop=1000001)))
for turn in range(10000000):
    cups2 = move(cups2, 1000000)
idx1 = np.where(cups2 == 1)[0]
next1, next2 = cups2[idx1+1], cups2[idx1+2]
print(f'PART TWO: {next1 * next2}')
