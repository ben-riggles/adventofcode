import numpy as np


with open('2020/day10/small.txt') as f:
    adapters = np.array([int(line) for line in f.read().splitlines()])

x = np.append(adapters, (0, max(adapters) + 3))

adapters = np.sort(np.append(adapters, (0, max(adapters) + 3)))
shifted = np.roll(adapters, 1)
diff = adapters[1:] - shifted[1:]  # type: ignore

ones, threes = np.count_nonzero(diff == 1), np.count_nonzero(diff == 3)
print(f'PART ONE: {ones * threes}')


def num_choices(ar, jolts) -> int:
    diffs = ar - jolts
    return np.count_nonzero((diffs >= 1) & (diffs <= 3))


#adapters[adapters == 1] = 3
print(adapters)
choices = np.array([num_choices(adapters, x) for x in adapters])
print(choices)
choices[choices == 1] = 0
print(choices)