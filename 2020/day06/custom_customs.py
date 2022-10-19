from typing import List, Set


def parse_group(group: str) -> List[Set[str]]:
    return [set(x) for x in group.split('\n')]


with open('2020/day06/data.txt') as f:
    groups = [parse_group(line) for line in f.read().split('\n\n')]

union = [set.union(*x) for x in groups]
print(f'PART ONE: {sum([len(x) for x in union])}')

intersection = [set.intersection(*x) for x in groups]
print(f'PART TWO: {sum([len(x) for x in intersection])}')
