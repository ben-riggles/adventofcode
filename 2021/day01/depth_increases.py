with open('2021/day01/depth_measurements.txt') as f:
    measurements = list(map(int, f.readlines()))

shifted = measurements[1:]
measurements = measurements[:-1]

count = 0
for left, right in zip(measurements, shifted):
    if right > left:
        count += 1

print(count)
