import numpy as np

class Line:
    def __init__(self, line_str):
        p1, p2 = line_str.split('->')
        x1, y1 = p1.split(',')
        x2, y2 = p2.split(',')

        self.x1 = int(x1.strip())
        self.y1 = int(y1.strip())
        self.x2 = int(x2.strip())
        self.y2 = int(y2.strip())

    def __str__(self):
        return f'({self.x1},{self.y1}) -> ({self.x2},{self.y2})'

    def flat(self):
        return (self.x1 == self.x2 or self.y1 == self.y2)

    def points(self):
        if self.x1 == self.x2:
            step = 1 if self.y2 > self.y1 else -1
            return [(self.x1, y) for y in range(self.y1, self.y2+step, step)]
        elif self.y1 == self.y2:
            step = 1 if self.x2 > self.x1 else -1
            return [(x, self.y1) for x in range(self.x1, self.x2+step, step)]
        else:
            # Diagonal line
            x_step = 1 if self.x2 > self.x1 else -1
            y_step = 1 if self.y2 > self.y1 else -1

            return [(x, y) for x, y in zip(range(self.x1, self.x2+x_step, x_step), range(self.y1, self.y2+y_step, y_step))]



with open('day05/vent_coordinates.txt') as f:
    line_strings = f.readlines()


lines = [Line(l) for l in line_strings]
point_dict = {}

for line in lines:
    for point in line.points():
        try:
            point_dict[point] += 1
        except KeyError:
            point_dict[point] = 1

overlaps = sum(1 for i in point_dict.values() if i >= 2)
print(overlaps)
