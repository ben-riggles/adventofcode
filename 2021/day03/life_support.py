import numpy as np

with open('day03/diagnostic_report.txt') as f:
    readings = f.read().splitlines()
    readings = np.asarray([int(x, 2) for x in readings])

oxygen = readings
for i in reversed(range(0, 12)):
    slicer = np.power(2, i)
    sliced = oxygen & slicer

    zeroes = (sliced == 0).sum()
    ones = (sliced > 0).sum()

    if ones >= zeroes:
        oxygen = oxygen[np.where(oxygen & slicer)]
    else:
        oxygen = oxygen[np.where((oxygen & slicer) == 0)]
    if len(oxygen) == 1:
        oxygen = oxygen[0]
        break


co2 = readings
for i in reversed(range(0, 12)):
    slicer = np.power(2, i)
    sliced = co2 & slicer

    zeroes = (sliced == 0).sum()
    ones = (sliced > 0).sum()

    if ones >= zeroes:
        co2 = co2[np.where((co2 & slicer) == 0)]
    else:
        co2 = co2[np.where(co2 & slicer)]
    if len(co2) == 1:
        co2 = co2[0]
        break

print(oxygen, co2)
print(oxygen * co2)
