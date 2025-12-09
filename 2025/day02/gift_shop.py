from __future__ import annotations
import aoc
from aoc.utils import Interval
from itertools import count
from typing import Generator


def invalid_ids(max_value: int) -> Generator[(int, int)]:
    max_digits = len(str(max_value))
    for i in count(1):
        s = str(i) * 2
        v = int(s)
        if v > max_value:
            return
        yield v, 1
        while len(s) <= max_digits:
            s += str(i)
            yield int(s), 2

def invalid_in_range(r: Interval, invalid_ids: list[int]) -> list[int]:
    try:
        start = next(i for i, x in enumerate(invalid_ids) if x >= r.start)
        end = next(i for i, x in enumerate(invalid_ids) if x > r.end)
    except StopIteration:
        return [0]
    
    in_range = invalid_ids[start:end]
    invalid_ids = invalid_ids[end:]
    return in_range


@aoc.register(__file__)
def answers():
    ranges = [Interval.parse(x) for x in aoc.read_data().replace('\n', '').split(',')]
    max_value = max(x.end for x in ranges)

    all_invalid = sorted(invalid_ids(max_value))
    invalid_1 = [x for x, part in all_invalid if part == 1]
    invalid_2 = [x for x, _ in all_invalid]

    result_1 = 0
    result_2 = 0
    for r in ranges:
        result_1 += sum(invalid_in_range(r, invalid_1))
        result_2 += sum(invalid_in_range(r, invalid_2))

    yield result_1
    yield result_2

if __name__ == '__main__':
    aoc.run()
