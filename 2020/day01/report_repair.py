import aoc
import itertools
from functools import reduce


def find_combo(data: list[int], target: int, len: int) -> int:
    for combo in itertools.combinations(data, len):
        if sum(combo) == target:
            return reduce(lambda x, y: x*y, combo)

def main():
    data = list(map(int, aoc.read_lines()))
    aoc.answer(1, find_combo(data, 2020, 2))
    aoc.answer(2, find_combo(data, 2020, 3))

if __name__ == '__main__':
    main()
