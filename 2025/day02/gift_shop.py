from __future__ import annotations
import aoc
from aoc.utils import Interval
from itertools import count
from typing import Generator


def parse_range(r: str) -> Interval:
    start, end = r.split('-')
    return Interval(int(start), int(end))

def invalid_ids(max_value: int, only_doubles: bool = True) -> Generator[int]:
    for value in count(1):
        for repeat in count(2):
            extended = int(str(value) * repeat)
            if extended > max_value:
                if repeat == 2:
                    return
                break
            yield extended

            if only_doubles:
                break

def in_ranges(ranges: list[Interval], value: int) -> bool:
    return any(value in x for x in ranges)


@aoc.register(__file__)
def answers():
    ranges = [parse_range(x) for x in aoc.read_data().replace('\n', '').split(',')]
    max_value = max(x.end for x in ranges)

    yield sum(set(x for x in invalid_ids(max_value) if in_ranges(ranges, x)))
    yield sum(set(x for x in invalid_ids(max_value, only_doubles=False) if in_ranges(ranges, x)))

if __name__ == '__main__':
    aoc.run()
