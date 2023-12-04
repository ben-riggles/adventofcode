from __future__ import annotations
import aoc
from collections import defaultdict
import itertools
import re
from typing import Generator


def adjacent_points(x: int, y_start: int, length: int) -> Generator[int, int]:
    yield from itertools.product(range(x-1, x+2), range(y_start-1, y_start+length+1))

GEAR = '*'

@aoc.register(__file__)
def answers():
    schematic = aoc.read_data()
    schematic_grid = schematic.splitlines()
    line_length = len(schematic_grid[0]) + 1

    non_symbols = {str(n) for n in range(10)} | {"."}
    gear_values = defaultdict(list)

    part_total = 0
    for _match in re.finditer(r'(\d+)', schematic):
        x, y = divmod(_match.start(), line_length)
        val = _match.group()
        for adj_x, adj_y in adjacent_points(x, y, len(val)):
            try:
                adj_val = schematic_grid[adj_x][adj_y]
            except IndexError:
                continue

            if adj_val not in non_symbols:
                val = int(val)
                part_total += val
                if adj_val == GEAR:
                    gear_values[(adj_x, adj_y)].append(val)
    yield part_total
    yield sum(v[0] * v[1] for v in gear_values.values() if len(v) == 2)


if __name__ == '__main__':
    aoc.run()
