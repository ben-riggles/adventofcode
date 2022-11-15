import aoc
import numpy as np
from numpy.typing import NDArray
from scipy.stats import mode


def calculate_ratings(data: NDArray) -> tuple[int]:
    gamma, epsilon = 0, 0
    oxygen, co2 = data.copy(), data.copy()
    for i in reversed(range(int(max(data)).bit_length())):
        bit = 2 ** i
        data_common = mode(data & bit, keepdims=True)[0][0]
        oxygen_common = mode(data & bit, keepdims=True)[0][0]
        co2_common = mode(data & bit, keepdims=True)[0][0]

        gamma += data_common
        epsilon += bit - data_common
        if len(oxygen) > 1:
            oxygen = oxygen[np.where((oxygen & bit) == oxygen_common)]
        if len(co2) > 1:
            co2 = co2[np.where((co2 & bit) == (bit - co2_common))]
    return gamma, epsilon, oxygen[0], co2[0]


@aoc.register(__file__)
def answers():
    data = np.array([int(x, 2) for x in aoc.read_lines()])
    gamma, epsilon, oxygen, co2 = calculate_ratings(data)
    
    yield gamma * epsilon
    yield oxygen * co2

if __name__ == '__main__':
    aoc.run()
