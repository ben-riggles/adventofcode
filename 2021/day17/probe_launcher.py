from typing import Tuple, List
import math

with open('2021/day17/target.txt') as f:
    target_str = f.read().strip()

asdf = None
asdf.fish


class TargetArea:
    def __init__(self, target_str:str):
        target_area = target_str.split(':')[1].strip()
        target_x, target_y = target_area.split(',')
        target_x = target_x.strip().split('=')[1].strip()
        target_y = target_y.strip().split('=')[1].strip()
        x_min, x_max = target_x.split('..')
        y_min, y_max = target_y.split('..')

        self.x_min:int = int(x_min)
        self.x_max:int = int(x_max)
        self.y_min:int = int(y_min)
        self.y_max:int = int(y_max)

        self.possible_x_vels = self.__possible_x_vels()
        self.possible_y_vels = self.__possible_y_vels(self.y_min, 3*self.x_max)

    def __repr__(self):
        return f'TargetArea(x=[{self.x_min}..{self.x_max}], y=[{self.y_min}..{self.y_max}])'

    def __contains__(self, point:Tuple[int, int]):
        return (self.x_min <= point[0] <= self.x_max) and (self.y_min <= point[1] <= self.y_max)

    def __possible_x_vels(self) -> List[int]:
        x_max, x_min = abs(self.x_max), abs(self.x_min)
        min_x_vel = math.ceil(-1 + math.sqrt(1 + 8 * x_min) / 2)

        possibilities = []
        for x_vel in range(min_x_vel, self.x_max+1):
            t = 0
            x_prev = None

            while True:
                x_pos = t * x_vel - (t * (t-1) / 2)
                if x_min <= x_pos <= x_max:
                    possibilities.append(x_vel)
                    break
                if x_prev and (x_pos == x_prev or x_pos > x_max):
                    break
                x_prev = x_pos
                t += 1
        if self.x_max < 0:
            possibilities = [-1*x for x in possibilities]
        return possibilities

    def __possible_y_vels(self, min_vel, max_vel) -> List[int]:
        possibilities = []
        for y_vel in range(min_vel, max_vel):
            t = 0
            y_prev = None

            while True:
                y_pos = t * y_vel - (t * (t-1) / 2)
                if self.y_min <= y_pos <= self.y_max:
                    possibilities.append(y_vel)
                    break
                if y_prev and y_pos < y_prev and y_pos < self.y_min:
                    break
                y_prev = y_pos
                t += 1
        return possibilities

targetArea = TargetArea(target_str)
print(targetArea)


class Probe:
    def __init__(self, x_vel:int, y_vel:int):
        self.x_vel:int = x_vel
        self.y_vel:int = y_vel
        self.trajectory:List[Tuple[int, int]] = []

    def __repr__(self):
        return f'Probe({self.x_vel}, {self.y_vel})'

    @property
    def max_height(self) -> int:
        return max([p[1] for p in self.trajectory])

    def position(self, time:int) -> Tuple[int, int]:
        if self.x_vel > 0:
            _time = time if time <= self.x_vel else self.x_vel
            x_pos = _time * self.x_vel - (_time * (_time-1) / 2)
        else:
            _time = time if time >= self.x_vel else self.x_vel
            x_pos = _time * self.x_vel + (_time * (_time-1) / 2)

        y_pos = time * self.y_vel - (time * (time-1) / 2)
        return (x_pos, y_pos)

    def launch(self, area:TargetArea) -> bool:
        t = 0
        prev:Tuple[int, int] = None

        while True:
            pos = self.position(time=t)
            self.trajectory.append(pos)
            if pos in area:
                return True

            if prev is not None:
                if self.x_vel > 0:
                    if (pos[0] == prev[0] and pos[0] < area.x_min) or pos[0] > area.x_max:
                        return False
                else:
                    if (pos[0] == prev[0] and pos[0] > area.x_max) or pos[0] < area.x_min:
                        return False
                if pos[1] < prev[1] and pos[1] < area.y_min:
                    return False
            prev = pos
            t += 1


successful_probes = []
for y_vel in targetArea.possible_y_vels:
    for x_vel in targetArea.possible_x_vels:
        p = Probe(x_vel, y_vel)
        if p.launch(targetArea):
            successful_probes.append(p)

print(successful_probes)
max_height = max([p.max_height for p in successful_probes])
print(f'{max_height=}')
print(f'Number of possibilities: {len(successful_probes)}')