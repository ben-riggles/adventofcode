from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270

    def __str__(self):
        return self.name[0]

    def __add__(self, deg):
        return Direction((self.value + deg) % 360)

    def __sub__(self, deg):
        return Direction((self.value - deg) % 360)


@dataclass
class Location:
    x: int = 0
    y: int = 0

    def __repr__(self):
        return f'Location({self.x}, {self.y})'

    def __add__(self, other: Location):
        return Location(x = self.x + other.x, y = self.y + other.y)

    def __sub__(self, other: Location):
        return Location(x = self.x - other.x, y = self.y - other.y)

    def __mul__(self, val: int):
        return Location(self.x * val, self.y * val)

    def rotate(self, deg: int, clockwise: bool = True) -> Location:
        if (deg == 90 and clockwise) or (deg == 270 and not clockwise):
            return Location(self.y, -self.x)
        elif (deg == 180):
            return Location(-self.x, -self.y)
        elif (deg == 270 and clockwise) or (deg == 90 and not clockwise):
            return Location(-self.y, self.x)
        raise ValueError(f'Invalid angle: {deg}')

    def manhattan_dist(self) -> int:
        return abs(self.x) + abs(self.y)


class Ferry:
    def __init__(self, direction: Direction = None, waypoint: Location = None):
        self.loc = Location(0, 0)
        self.direction = direction
        self.waypoint = waypoint
        if not (self.direction is not None) ^ (self.waypoint is not None):
            raise Exception('Ferry must have a cardinal direction or waypoint provided')

    def move(self, command):
        cmd, val = command[0], int(command[1:])
        self._move_direct(cmd, val) if self.waypoint is None else self._move_relative(cmd, val)

    def _move_direct(self, cmd, val):
        match cmd:
            case 'N': self.loc += Location(0, val)
            case 'E': self.loc += Location(val, 0)
            case 'S': self.loc += Location(0, -val)
            case 'W': self.loc += Location(-val, 0)
            case 'L': self.direction -= val
            case 'R': self.direction += val
            case 'F': self._move_direct(str(self.direction), val)
            case _: raise Exception(f'Invalid command {cmd}')

    def _move_relative(self, cmd, val):
        match cmd:
            case 'N': self.waypoint += Location(0, val)
            case 'E': self.waypoint += Location(val, 0)
            case 'S': self.waypoint += Location(0, -val)
            case 'W': self.waypoint += Location(-val, 0)
            case 'L': self.waypoint = self.waypoint.rotate(val, clockwise=False)
            case 'R': self.waypoint = self.waypoint.rotate(val, clockwise=True)
            case 'F': self.loc += self.waypoint * val
            case _: raise Exception(f'Invalid command {cmd}')


with open('2020/day12/data.txt') as f:
    commands = f.read().splitlines()

ferry = Ferry(direction=Direction.EAST)
[ferry.move(cmd) for cmd in commands]
print(f'PART ONE: {ferry.loc.manhattan_dist()}')

ferry = Ferry(waypoint=Location(10, 1))
[ferry.move(cmd) for cmd in commands]
print(f'PART ONE: {ferry.loc.manhattan_dist()}')
