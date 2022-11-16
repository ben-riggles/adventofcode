import aoc
import numpy as np
from numpy.typing import NDArray
from scipy.stats import mode


def most_common(data: NDArray) -> int:
    zeroes = (data == 0).sum()
    ones = (data > 0).sum()
    return 1 if ones >= zeroes else 0
    return mode(data, keepdims=True)[0][0]

def bits_to_int(data: NDArray) -> int:
    return data.dot(1 << np.arange(data.shape[-1] - 1, -1, -1))

def reduce_data(data: NDArray, common=True) -> int:
    retval = data.copy()
    for idx in range(data.shape[1]):
        column = retval[:,idx]
        common_value = most_common(column)

        print(len(retval), common_value)

        if common:
            retval = retval[np.where(column == common_value)]
        else:
            retval = retval[np.where(column == (1 - common_value))]
        if len(retval) == 1:
            return bits_to_int(retval[0])
    return None


@aoc.register(__file__)
def answers():
    data = np.array([list(map(int, x)) for x in aoc.read_lines()])

    gamma = np.array([most_common(data[:,x]) for x in range(data.shape[1])])
    epsilon = 1 - gamma
    yield bits_to_int(gamma) * bits_to_int(epsilon)

    oxygen = reduce_data(data)
    co2 = reduce_data(data, common=False)
    print(oxygen, co2)
    yield oxygen * co2

if __name__ == '__main__':
    aoc.run()
