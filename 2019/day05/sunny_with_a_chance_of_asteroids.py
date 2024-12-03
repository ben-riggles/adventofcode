import aoc
import itertools
from operator import add, mul, lt, eq


def run(intcode: list[int], input: int = 1) -> int:
    _intcode = intcode[:]

    pointer = 0
    outputs = []

    def _param(id: int, mode: int):
        try:
            match mode:
                case 0: return _intcode[_intcode[pointer+id]]
                case 1: return _intcode[pointer+id]
                case _: raise Exception("Invalid mode detected")
        except IndexError:
            return None

    while _intcode[pointer] != 99:
        instruction = str(_intcode[pointer]).zfill(5)
        opcode = int(instruction[3:])
        modes = tuple(map(int, reversed(instruction[:3])))
        args = [_param(i+1, m) for i, m in enumerate(modes)]
        
        match opcode:
            case 1 | 2:
                op = add if opcode == 1 else mul
                left = _intcode[_intcode[pointer+1]] if modes[0] == 0 else _intcode[pointer+1]
                right = _intcode[_intcode[pointer+2]] if modes[1] == 0 else _intcode[pointer+2]

                if modes[2] == 0:
                    _intcode[_intcode[pointer+3]] = op(left, right)
                else:
                    _intcode[pointer+3] = op(left, right)
                
                pointer += 4
            case 3:
                x = _intcode[pointer+1]
                _intcode[x] = input
                # arg = _intcode[_intcode[pointer+1]] if args[0] == 0 else _intcode[pointer+1]
                # _intcode[arg] = input
                pointer += 2
            case 4:
                arg = _intcode[_intcode[pointer+1]] if modes[0] == 0 else _intcode[pointer+1]
                outputs.append(arg)
                pointer += 2
            case 5:
                left = _intcode[_intcode[pointer+1]] if modes[0] == 0 else _intcode[pointer+1]
                right = _intcode[_intcode[pointer+2]] if modes[1] == 0 else _intcode[pointer+2]
                
                if left > 0:
                    pointer = right
                else:
                    pointer += 3
            case 6:
                left = _intcode[_intcode[pointer+1]] if modes[0] == 0 else _intcode[pointer+1]
                right = _intcode[_intcode[pointer+2]] if modes[1] == 0 else _intcode[pointer+2]

                if left == 0:
                    pointer = right
                else:
                    pointer += 3
            case 7 | 8:
                op = lt if opcode == 7 else eq
                left = _intcode[_intcode[pointer+1]] if modes[0] == 0 else _intcode[pointer+1]
                right = _intcode[_intcode[pointer+2]] if modes[1] == 0 else _intcode[pointer+2]
                value = 1 if op(left, right) else 0

                if modes[2] == 0:
                    _intcode[_intcode[pointer+3]] = value
                else:
                    _intcode[pointer+3] = value
                pointer += 4
            case _:
                raise Exception("Invalid opcode detected")
            
    return outputs[-1]

@aoc.register(__file__)
def answers():
    intcode = list(map(int, aoc.read_data().split(',')))
    yield run(intcode, input=1)
    yield run(intcode, input=5)

if __name__ == '__main__':
    aoc.run()
