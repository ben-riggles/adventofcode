import aoc
import numpy as np


@aoc.register(__file__)
def answers():
    cubes = np.array([tuple(map(int, line.split(','))) for line in aoc.read_lines('small')])
    print(cubes)
    print(cubes + (1,0,0))
    

if __name__ == '__main__':
    aoc.run()
