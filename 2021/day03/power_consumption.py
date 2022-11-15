import numpy as np
from scipy.stats import mode

with open('2021/day03/diagnostic_report.txt') as f:
    readings = np.asarray(f.read().splitlines())
    readings = [int(x, 2) for x in readings]

gamma = 0
epsilon = 0
for i in range(0, 12):
    slicer = np.power(2, i)
    sliced = readings & slicer

    zeroes = (sliced == 0).sum()
    ones = (sliced > 0).sum()

    if zeroes > ones:
        gamma += slicer
    elif ones > zeroes:
        epsilon += slicer
    else:
        print('uhhhhhhhhh')

print(gamma, epsilon)
print(gamma*epsilon)
