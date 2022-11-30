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

    def velocities(self) -> Generator[tuple[int,int]]:
        # Quadratic equation to solve triangular number
        #  x = m*(m+1)/2
        min_x_vel = math.ceil(-1 + math.sqrt(1 + 8 * abs(self.x_min)) / 2)
        step = 1 if self.x_min >=0 else -1

        for x_vel in range(min_x_vel, self.x_max+step, step):
            t_vals = np.arange(1, x_vel+step)
            x_velos = t_vals[::-1]
            x_vals = np.cumsum(x_velos)
            idxs = np.where((x_vals >= self.x_min) & (x_vals <= self.x_max))
            for t, x in zip(t_vals[idxs], x_vals[idxs]):
                y_vel_min = (self.y_min + (t * (t-1) / 2)) / t
                y_vel_min = math.floor(y_vel_min) if y_vel_min >= 0 else math.ceil(y_vel_min)
                y_vel_max = (self.y_max + (t * (t-1) / 2)) / t
                y_vel_max = math.floor(y_vel_max) if y_vel_max >= 0 else math.ceil(y_vel_max)
                y_pos_min =  t * y_vel_min - (t * (t-1) / 2)
                y_pos_max =  t * y_vel_max - (t * (t-1) / 2)
                yield from [(x, y) for y in range(y_vel_min, y_vel_max)]

    @staticmethod
    def from_string(target_str: str) -> Target:
        m = re.match(r'target area: x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+), y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+)', target_str)
        return Target(**{k: int(v) for k, v in m.groupdict().items()})
        
def highest_y(y_vel: int) -> int:
    if y_vel > 0:
        return int((y_vel * (y_vel + 1)) / 2)
    return 0


@aoc.register(__file__)
def answers():
    target = Target.from_string(aoc.read_data('small'))
    for x in target.velocities():
        print(x)
    high_points = [highest_y(y_vel) for _, y_vel in target.velocities()]

    yield max(high_points)
    yield len(high_points)

if __name__ == '__main__':
    print(math.floor(0.5))
    aoc.run()
