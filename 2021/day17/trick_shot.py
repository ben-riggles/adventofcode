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

    def _y_velocities(self) -> dict[int, set]:
        min_y_vel = math.ceil(-1 + math.sqrt(1 + 8 * abs(self.x_min)) / 2) if self.y_min >= 0 else self.y_min
        max_y_vel = self.y_max + 1 if self.y_max >= 0 else -self.y_min - 1

        y_vel_dict = {}
        for y_vel in range(min_y_vel, max_y_vel+1):
            max_t = math.floor(((2*y_vel + 1) + math.sqrt((2*y_vel + 1)**2 - 8*self.y_min)) / 2)
            t_vals = np.arange(1, max_t+1)
            y_vals = ((y_vel * t_vals) - ((t_vals * (t_vals - 1)) / 2)).astype(int)
            idxs = np.where((y_vals >= self.y_min) & (y_vals <= self.y_max))[0]
            if idxs.size != 0:
                y_vel_dict[y_vel] = set(t_vals[idxs])
        return y_vel_dict

    def _x_velocities(self, max_t: int) -> dict[int, set]:
        min_x_vel = math.ceil(-1 + math.sqrt(1 + 8 * abs(self.x_min)) / 2)
        step = 1 if self.x_min >=0 else -1
        max_x_vel = self.x_max + step

        x_vel_dict = {}
        for x_vel in range(min_x_vel, max_x_vel, step):
            t_vals = np.arange(1, x_vel+step)
            x_vals = np.cumsum(t_vals[::-1])
            idxs = np.where((x_vals >= self.x_min) & (x_vals <= self.x_max))[0]
            valid_t = set(t_vals[idxs])
            if idxs.size != 0:
                if (len(x_vals) - 1) in idxs:
                    valid_t |= set(range(len(x_vals), max_t+1))
                x_vel_dict[x_vel] = valid_t
        return x_vel_dict


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
    asdf = target._y_velocities()
    max_t = max(set.union(*[v for v in asdf.values()]))
    qwer = target._x_velocities(max_t)
    raise
    for x in target.velocities():
        print(x)
    high_points = [highest_y(y_vel) for _, y_vel in target.velocities()]

    yield max(high_points)
    yield len(high_points)

if __name__ == '__main__':
    print(math.floor(0.5))
    aoc.run()
