import numpy as np

with open('day13/code_sheet.txt') as f:
    lines = f.read().splitlines()
blank_idx = lines.index('')
points = lines[:blank_idx]
points = np.array([np.array(x.split(','), int) for x in points], dtype=int).T
folds = lines[blank_idx+1:]
print(points)


# Part 1
print('---------- Part 1 ----------')
for fold in folds:
    print(fold)
    axis, line = fold.replace('fold along ', '').split('=')
    line = int(line)

    idx = 0 if axis == 'x' else 1
    points[idx] = line - abs(points[idx] - line)
    points = np.unique(points.T, axis=0).T

print(points.T)
print(len(points.T))


# Part 2
print('---------- Part 2 ----------')
code = np.full((np.max(points[0]+1), np.max(points[1]+1)), '.')
code[tuple(points[0]), tuple(points[1])] = '#'
print(code)
