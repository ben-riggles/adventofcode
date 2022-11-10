
from itertools import count
import time

start = time.process_time()

with open('2020/day03/data.txt') as f:
    fin = f.read().splitlines()

grid = [l.rstrip() for l in fin]
height, width = len(grid), len(grid[0])
trees = 0

for row, col in zip(range(height), count(0, 3)):
	if grid[row][col % width] == '#':
		trees += 1

print(trees)


total = trees

for dr, dc in ((1, 1), (1, 5), (1, 7), (2, 1)):
	trees = 0

	for row, col in zip(range(0, height, dr), count(0, dc)):
		if grid[row][col % width] == '#':
			trees += 1

	total *= trees

print(total)

print(time.process_time() - start)