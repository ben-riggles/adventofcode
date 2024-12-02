import aoc
import itertools
from operator import add, mul


def run(intcode: list[int], input: int = 1) -> int:
    _intcode = intcode[:]

    pointer = 0
    outputs = []

    def _param(id: int, mode: int):
        print(id, mode, _intcode[pointer+id])
        match mode:
            case 0: return _intcode[_intcode[pointer+id]]
            case 1: return _intcode[pointer+id]
            case _: raise Exception("Invalid mode detected")

    while _intcode[pointer] != 99:
        instruction = str(_intcode[pointer]).zfill(5)
        opcode = int(instruction[3:])
        args = tuple(map(int, reversed(instruction[:3])))
        
        match opcode:
            case 1 | 2:
                op = add if opcode == 1 else mul
                x, y, z = _param(1, args[0]), _param(2, args[1]), _param(3, args[2])
                _intcode[z] = op(x, y)
                pointer += 4
            case 3:
                _intcode[_param(1, args[0])] = input
                pointer += 2
            case 4:
                outputs.append(_intcode[_param(1, args[0])])
                pointer += 2
            case _:
                raise Exception("Invalid opcode detected")
    print(outputs)
    return _intcode[0]

@aoc.register(__file__)
def answers():
    intcode = list(map(int, aoc.read_data().split(',')))
    yield run(intcode, input=1)

if __name__ == '__main__':
    aoc.run()
