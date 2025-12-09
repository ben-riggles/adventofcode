from __future__ import annotations
import aoc
from aoc.utils import Interval
from itertools import count
from typing import Generator


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
    ranges = [Interval.parse(x) for x in aoc.read_data().replace('\n', '').split(',')]
    max_value = max(x.end for x in ranges)
    max_digits = len(str(max_value))

    invalid_1 = set()
    invalid_2 = set()
    for i in count(1):
        s = str(i) * 2
        v = int(s)
        if v > max_value:
            break
        invalid_1.add(v)
        while len(s) <= max_digits:
            invalid_2.add(int(s))
            s += str(i)
    invalid_1 = sorted(invalid_1)
    invalid_2 = sorted(invalid_2)
    ranges = sorted(ranges, key=lambda x: x.start)

    a = 0
    b = 0
    for r in ranges:
        try:
            invalid_start_1 = next(i for i, x in enumerate(invalid_1) if x >= r.start)
            invalid_end_1 = next(i for i, x in enumerate(invalid_1) if x > r.end)
            _invalid_1 = invalid_1[invalid_start_1:invalid_end_1]
            invalid_1 = invalid_1[invalid_end_1:]
            a += sum(_invalid_1)
        except StopIteration:
            pass

        try:
            invalid_start_2 = next(i for i, x in enumerate(invalid_2) if x >= r.start)
            invalid_end_2 = next(i for i, x in enumerate(invalid_2) if x > r.end)
            _invalid_2 = invalid_2[invalid_start_2:invalid_end_2]
            invalid_2 = invalid_2[invalid_end_2:]
            b += sum(_invalid_2)
        except StopIteration:
            pass
    yield a
    yield b

if __name__ == '__main__':
    aoc.run()
