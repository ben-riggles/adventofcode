from __future__ import annotations
import aoc
from aoc.utils import Interval
from dataclasses import dataclass
import itertools
import re
from typing import Generator
    

@dataclass
class Zone:
    x: Interval
    y: Interval
    z: Interval

    def intersection(self, other: Zone) -> Zone:
        return Zone(x=self.x & other.x, y = self.y & other.y, z=self.z & other.z)
    
    def union(self, other: Zone) -> Generator[Zone]:
        pass

    def points(self) -> Generator[tuple[int, int, int]]:
        yield from itertools.product(self.x, self.y, self.z)
    

def parse_line(line: str) -> tuple[Zone, bool]:
    m = re.match(r'(?P<state>on|off) x=(?P<min_x>\d+)..(?P<max_x>\d+),y=(?P<min_y>\d+)..(?P<max_y>\d+),z=(?P<min_z>\d+)..(?P<max_z>\d+)', line).groupdict()
    zone = Zone(
        x = Interval(int(m['min_x']), int(m['max_x'])),
        y = Interval(int(m['min_y']), int(m['max_y'])),
        z = Interval(int(m['min_z']), int(m['max_z']))
    )
    return zone, m['state'] == 'on'


@aoc.register(__file__)
def answers():
    instructions = [parse_line(x) for x in aoc.read_lines('small')]
    zone = None
    
    for z, state in instructions:
        if state:
            if zone is None:
                zone = z
            else:
                pass


if __name__ == '__main__':
    aoc.run()
