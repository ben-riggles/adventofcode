import numpy as np
import functools
from collections import Counter

with open('day14/polymer_template.txt') as f:
    lines = f.read().splitlines()

polymer = lines[0].strip()
lines = [tuple(x.split(' -> ')) for x in lines[2:]]
rules = {(x[0][0], x[0][1]): x[1] for x in lines}
better_rules = {(x[0][0], x[0][1]): [(x[0][0], x[1]), (x[1], x[0][1])] for x in lines}


# Part 1
print('---------- Part 1 ----------')
def new_pairs(pair_list):
    retval = []
    for pair in pair_list:
        retval.extend(better_rules[pair])
    return retval

pairs = [(polymer[x-1], polymer[x]) for x in range(1, len(polymer))]
for x in range(10):
    pairs = new_pairs(pairs)

final_polymer = np.array([x[0] for x in pairs] + [pairs[-1][1]])
unique_values = np.unique(final_polymer)
counts = {x: len(final_polymer[final_polymer == x]) for x in unique_values}
v = counts.values()
print(counts)
print(max(v) - min(v))


# Part 2
print('---------- Part 2 ----------')

@functools.cache
def split_pair(pair, remainder):
    first, second = better_rules[pair]
    remainder -= 1

    if remainder == 0:
        return Counter([first[0], second[0]])
    return split_pair(first, remainder) + split_pair(second, remainder)

pairs = [(polymer[x-1], polymer[x]) for x in range(1, len(polymer))]
counts = Counter()
for pair in pairs:
    counts.update(split_pair(pair, 40))

counts.update(pairs[-1][1])
v = counts.values()
print(counts)
print(max(v) - min(v))
