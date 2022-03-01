import numpy as np

with open('day01/depth_measurements.txt') as f:
    measurements = np.asarray(list(map(int, f.readlines())))

w1 = measurements[:-2]
w2 = measurements[1:-1]
w3 = measurements[2:]

windows = w1 + w2 + w3
shifted = windows[1:]
windows = windows[:-1]

count = 0
for left, right in zip(windows, shifted):
    if right > left:
        count += 1

print(count)
