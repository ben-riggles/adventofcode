from __future__ import annotations
import aoc
from dataclasses import dataclass, field
import math
import numpy as np
import re
from typing import Generator


@dataclass
class Target:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def __contains__(self, point: tuple[int,int]):
        return (self.x_min <= point[0] <= self.x_max) and (self.y_min <= point[1] <= self.y_max)

    def _x_velocities(self) -> list[int]:
        min_x_vel = math.ceil(-1 + math.sqrt(1 + 8 * abs(self.x_min)) / 2)
        step = 1 if self.x_min >=0 else -1

        possibilities = []
        for x_vel in range(min_x_vel, self.x_max+step, step):
            t = np.arange(x_vel+step)
            x_velos = t[::-1]
            x_vals = np.cumsum(x_velos)
            asdf = np.vstack((t, x_vals)).T
            asdf = asdf[(asdf[:,1] >= self.x_min) & (asdf[:,1] <= self.x_max)]
            possibilities.extend(tuple(x) for x in asdf if self.x_min <= x[1] <= self.x_max)
        return possibilities

    def _y_velocities(self, possibilities: tuple[int,int]) -> list[int]:
        pass

    @staticmethod
    def from_string(target_str: str) -> Target:
        m = re.match(r'target area: x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+), y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+)', target_str)
        return Target(**{k: int(v) for k, v in m.groupdict().items()})

class Shot:
    pass



@aoc.register(__file__)
def answers():
    target = Target.from_string(aoc.read_data())
    print(target)
    print(target._x_velocities())
    raise

if __name__ == '__main__':
    aoc.run()
